import { createServer, type IncomingMessage, type ServerResponse } from "node:http";
import { appendFile, mkdir, realpath } from "node:fs/promises";
import { createHash, timingSafeEqual, randomUUID } from "node:crypto";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import path from "node:path";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";
import { z } from "zod";

const execFileAsync = promisify(execFile);
const NAME = "tce-vps-control-mcp";
const VERSION = "0.1.0";
const HOST = process.env.HOST ?? "127.0.0.1";
const PORT = Number(process.env.PORT ?? "8765");
const TOKEN = process.env.MCP_BEARER_TOKEN ?? "";
const AUDIT_FILE = process.env.AUDIT_FILE ?? "/var/log/tce-vps-control-mcp/audit.jsonl";
const KUBECTL = process.env.KUBECTL_PATH ?? "/usr/local/bin/kubectl";
const KUBECONFIG = process.env.KUBECONFIG ?? "/etc/tce-vps-control-mcp/kubeconfig";
const MAX_COMMAND_MS = 60_000;
const MAX_OUTPUT = 256 * 1024;
const COMMAND_MAX_LENGTH = 4_000;
const ROOTS = (process.env.ALLOWED_CWD_ROOTS ?? "/srv,/var/log,/tmp")
  .split(",").map((entry) => path.resolve(entry.trim())).filter(Boolean);

if (TOKEN.length < 48) {
  throw new Error("MCP_BEARER_TOKEN must be a randomly generated secret of at least 48 characters.");
}
if (!Number.isInteger(PORT) || PORT < 1 || PORT > 65535) {
  throw new Error("PORT must be a valid TCP port.");
}

type AuditRecord = {
  timestamp: string;
  requestId: string;
  actor: string;
  operation: string;
  outcome: "started" | "success" | "error";
  durationMs?: number;
  exitCode?: number;
  commandSha256?: string;
};

async function audit(record: AuditRecord): Promise<void> {
  await mkdir(path.dirname(AUDIT_FILE), { recursive: true, mode: 0o700 });
  await appendFile(AUDIT_FILE, JSON.stringify(record) + "\n", { mode: 0o600 });
}

function safeEqual(left: string, right: string): boolean {
  const a = Buffer.from(left);
  const b = Buffer.from(right);
  return a.length === b.length && timingSafeEqual(a, b);
}

function authorized(req: IncomingMessage): boolean {
  const header = req.headers.authorization ?? "";
  if (!header.startsWith("Bearer ")) return false;
  return safeEqual(header.slice(7), TOKEN);
}

function redact(value: string): string {
  return value
    .replace(/(Bearer\s+)[A-Za-z0-9._~+/-]+=*/gi, "$1[REDACTED]")
    .replace(/((?:password|passwd|secret|token|api[_-]?key)\s*[=:]\s*)[^\s,;]+/gi, "$1[REDACTED]")
    .replace(/(postgres(?:ql)?:\/\/[^:\s/]+:)[^@\s]+@/gi, "$1[REDACTED]@");
}

function boundedOutput(value: string): string {
  const safe = redact(value);
  return safe.length > MAX_OUTPUT
    ? safe.slice(0, MAX_OUTPUT) + "\n[output truncated]"
    : safe;
}

function validateName(value: string, label: string): string {
  if (!/^[a-zA-Z0-9][a-zA-Z0-9_.-]{0,127}$/.test(value)) {
    throw new Error(`Invalid ${label}.`);
  }
  return value;
}

function validateNamespace(value: string): string {
  if (!/^[a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?$/.test(value)) {
    throw new Error("Invalid Kubernetes namespace.");
  }
  return value;
}

async function validateCwd(input?: string): Promise<string> {
  const requested = path.resolve(input ?? ROOTS[0] ?? "/srv");
  const cwd = await realpath(requested);
  const allowedRoots = await Promise.all(ROOTS.map(async (root) => {
    try {
      return await realpath(root);
    } catch {
      return null;
    }
  }));
  const allowed = allowedRoots.some((root) =>
    root !== null && (cwd === root || cwd.startsWith(root + path.sep))
  );
  if (!allowed) throw new Error("Working directory resolves outside ALLOWED_CWD_ROOTS.");
  return cwd;
}

function assertSafeShell(command: string): void {
  if (!command.trim() || command.length > COMMAND_MAX_LENGTH) {
    throw new Error(`Command must contain 1-${COMMAND_MAX_LENGTH} characters.`);
  }
  const forbidden = [
    /(^|[;&|\s])sudo([\s;&|]|$)/i,
    /(^|[;&|\s])kubectl([\s;&|]|$)/i,
    /(^|[;&|\s])docker([\s;&|]|$)/i,
    /\b(mkfs(?:\.[a-z0-9]+)?|fdisk|parted|wipefs|shutdown|reboot|poweroff|init\s+0)\b/i,
    /:\s*\(\)\s*\{/,
    /\brm\s+-[^\n]*\b--no-preserve-root\b/i,
    /\bdd\s+if=/i,
    />\s*\/dev\/(sd[a-z]|nvme|vd[a-z])/i
  ];
  if (forbidden.some((pattern) => pattern.test(command))) {
    throw new Error("Command rejected by the host safety policy. Use read-only diagnostics; production mutations must go through Platform reconcile-vps.yml.");
  }
}

async function run(
  file: string,
  args: string[],
  options: { cwd?: string; timeout?: number; env?: NodeJS.ProcessEnv; uid?: number; gid?: number } = {}
): Promise<{ stdout: string; stderr: string; exitCode: number }> {
  try {
    const result = await execFileAsync(file, args, {
      ...(options.cwd ? { cwd: options.cwd } : {}),
      timeout: Math.min(options.timeout ?? 15_000, MAX_COMMAND_MS),
      maxBuffer: MAX_OUTPUT,
      windowsHide: true,
      env: {
        PATH: process.env.PATH ?? "/usr/local/bin:/usr/bin:/bin",
        HOME: process.env.HOME ?? "/var/lib/tce-vps-control-mcp",
        LANG: "C.UTF-8",
        ...(options.env ?? {})
      }
    });
    return { stdout: boundedOutput(result.stdout), stderr: boundedOutput(result.stderr), exitCode: 0 };
  } catch (error) {
    const e = error as NodeJS.ErrnoException & { stdout?: string; stderr?: string; code?: number | string };
    return {
      stdout: boundedOutput(e.stdout ?? ""),
      stderr: boundedOutput(e.stderr ?? e.message ?? "Command failed."),
      exitCode: typeof e.code === "number" ? e.code : 1
    };
  }
}

async function executeAudited(
  operation: string,
  commandFingerprint: string | undefined,
  work: () => Promise<{ stdout: string; stderr: string; exitCode: number }>
) {
  const requestId = randomUUID();
  const actor = "mcp-bearer";
  const startedAt = Date.now();
  await audit({
    timestamp: new Date().toISOString(), requestId, actor, operation,
    outcome: "started", ...(commandFingerprint ? { commandSha256: commandFingerprint } : {})
  });
  try {
    const result = await work();
    await audit({
      timestamp: new Date().toISOString(), requestId, actor, operation,
      outcome: result.exitCode === 0 ? "success" : "error",
      durationMs: Date.now() - startedAt, exitCode: result.exitCode,
      ...(commandFingerprint ? { commandSha256: commandFingerprint } : {})
    });
    return result;
  } catch (error) {
    await audit({
      timestamp: new Date().toISOString(), requestId, actor, operation,
      outcome: "error", durationMs: Date.now() - startedAt,
      ...(commandFingerprint ? { commandSha256: commandFingerprint } : {})
    });
    throw error;
  }
}

function resultText(result: { stdout: string; stderr: string; exitCode: number }) {
  return {
    content: [{
      type: "text" as const,
      text: [
        `exit_code: ${result.exitCode}`,
        result.stdout ? `stdout:\n${result.stdout}` : "",
        result.stderr ? `stderr:\n${result.stderr}` : ""
      ].filter(Boolean).join("\n\n")
    }],
    isError: result.exitCode !== 0
  };
}

function createMcpServer(): McpServer {
  const server = new McpServer({ name: NAME, version: VERSION });

  server.registerTool("host_status", {
    description: "Read host health: uptime, memory, filesystem capacity and kernel. Read-only.",
    inputSchema: {}
  }, async () => {
    const result = await executeAudited("host_status", undefined, async () => {
      const commands = [
        ["uptime", []],
        ["free", ["-h"]],
        ["df", ["-hT"]],
        ["uname", ["-a"]]
      ] as const;
      const chunks: string[] = [];
      let exitCode = 0;
      for (const [file, args] of commands) {
        const item = await run(file, [...args]);
        chunks.push(`$ ${file} ${args.join(" ")}\n${item.stdout}${item.stderr}`);
        if (item.exitCode !== 0) exitCode = item.exitCode;
      }
      return { stdout: chunks.join("\n"), stderr: "", exitCode };
    });
    return resultText(result);
  });

  server.registerTool("shell_execute", {
    description: "Execute a shell command as the separate unprivileged tce-shell OS account. It has no sudoers entry, Docker group membership or Kubernetes kubeconfig. Arbitrary shell syntax is supported within the OS permissions of tce-shell. Use only when the user explicitly requested the command. Output is truncated and secrets are redacted.",
    inputSchema: {
      command: z.string().min(1).max(COMMAND_MAX_LENGTH),
      cwd: z.string().optional(),
      timeoutMs: z.number().int().min(1_000).max(MAX_COMMAND_MS).optional()
    }
  }, async ({ command, cwd, timeoutMs }) => {
    assertSafeShell(command);
    const workingDirectory = await validateCwd(cwd);
    const fingerprint = createHash("sha256").update(command).digest("hex");
    const result = await executeAudited("shell_execute", fingerprint, () =>
      run("/usr/bin/sudo", ["-n", "-u", "tce-shell", "-H", "--", "/bin/bash", "-lc", command], {
        cwd: workingDirectory,
        timeout: timeoutMs ?? 15_000,
        env: { HOME: "/var/lib/tce-shell" }
      })
    );
    return resultText(result);
  });

  server.registerTool("docker_ps", {
    description: "List Docker containers through the root-owned, argument-validating host wrapper. Read-only.",
    inputSchema: {}
  }, async () => {
    const result = await executeAudited("docker_ps", undefined, () =>
      run("/usr/bin/sudo", ["-n", "/usr/local/sbin/tce-mcp-docker", "ps"])
    );
    return resultText(result);
  });

  server.registerTool("docker_logs", {
    description: "Read the last lines of a Docker container log. Container name/ID and tail are validated by the server and host wrapper.",
    inputSchema: {
      container: z.string().min(1).max(128),
      tail: z.number().int().min(1).max(1000).default(200)
    }
  }, async ({ container, tail }) => {
    validateName(container, "container");
    const result = await executeAudited("docker_logs", undefined, () =>
      run("/usr/bin/sudo", ["-n", "/usr/local/sbin/tce-mcp-docker", "logs", container, String(tail)])
    );
    return resultText(result);
  });

  server.registerTool("k8s_get", {
    description: "Read Kubernetes resources across namespaces. Supported resources: pods, deployments, services, nodes, namespaces, events, replicasets.",
    inputSchema: {
      resource: z.enum(["pods", "deployments", "services", "nodes", "namespaces", "events", "replicasets"]),
      namespace: z.string().optional()
    }
  }, async ({ resource, namespace }) => {
    const args = ["get", resource, "-o", "wide"];
    if (namespace) args.push("-n", validateNamespace(namespace));
    else args.push("-A");
    const result = await executeAudited("k8s_get", undefined, () =>
      run(KUBECTL, args, { timeout: 20_000, env: { KUBECONFIG } })
    );
    return resultText(result);
  });

  server.registerTool("k8s_logs", {
    description: "Read logs for a Kubernetes pod. Namespace, pod and optional container are validated; output is bounded.",
    inputSchema: {
      namespace: z.string().min(1).max(63),
      pod: z.string().min(1).max(253),
      container: z.string().min(1).max(128).optional(),
      tail: z.number().int().min(1).max(2000).default(200),
      previous: z.boolean().default(false)
    }
  }, async ({ namespace, pod, container, tail, previous }) => {
    validateNamespace(namespace);
    if (!/^[a-z0-9]([a-z0-9.-]{0,251}[a-z0-9])?$/.test(pod)) throw new Error("Invalid pod name.");
    const args = ["logs", pod, "-n", namespace, "--tail", String(tail), "--all-containers=true"];
    if (container) args.push("-c", validateName(container, "container"));
    if (previous) args.push("--previous");
    const result = await executeAudited("k8s_logs", undefined, () =>
      run(KUBECTL, args, { timeout: 20_000, env: { KUBECONFIG } })
    );
    return resultText(result);
  });

  server.registerTool("systemd_status", {
    description: "Read the active/inactive status of an allowlisted host service. Read-only.",
    inputSchema: {
      service: z.enum(["k3s", "containerd", "docker", "nginx", "cloudflared"])
    }
  }, async ({ service }) => {
    const result = await executeAudited("systemd_status", undefined, () =>
      run("/usr/bin/systemctl", ["is-active", service])
    );
    return resultText(result);
  });

  return server;
}

const rateBuckets = new Map<string, { count: number; resetAt: number }>();
function rateLimited(ip: string): boolean {
  const now = Date.now();
  const current = rateBuckets.get(ip);
  if (!current || current.resetAt <= now) {
    rateBuckets.set(ip, { count: 1, resetAt: now + 60_000 });
    return false;
  }
  current.count += 1;
  return current.count > 60;
}

function sendJson(res: ServerResponse, status: number, body: unknown): void {
  res.writeHead(status, {
    "content-type": "application/json; charset=utf-8",
    "cache-control": "no-store",
    "x-content-type-options": "nosniff"
  });
  res.end(JSON.stringify(body));
}

async function readJson(req: IncomingMessage): Promise<unknown> {
  const chunks: Buffer[] = [];
  let size = 0;
  for await (const chunk of req) {
    const buffer = Buffer.isBuffer(chunk) ? chunk : Buffer.from(chunk);
    size += buffer.length;
    if (size > 1_048_576) throw new Error("Request body exceeds 1 MiB.");
    chunks.push(buffer);
  }
  if (!chunks.length) return undefined;
  return JSON.parse(Buffer.concat(chunks).toString("utf8"));
}

const httpServer = createServer(async (req, res) => {
  const url = new URL(req.url ?? "/", `http://${req.headers.host ?? "localhost"}`);
  if (url.pathname === "/healthz" && req.method === "GET") {
    sendJson(res, 200, { status: "ok", name: NAME, version: VERSION });
    return;
  }
  if (url.pathname !== "/mcp") {
    sendJson(res, 404, { error: "not_found" });
    return;
  }
  const ip = req.socket.remoteAddress ?? "unknown";
  if (rateLimited(ip)) {
    sendJson(res, 429, { error: "rate_limited" });
    return;
  }
  if (!authorized(req)) {
    sendJson(res, 401, { error: "unauthorized" });
    return;
  }
  if (req.method !== "POST") {
    res.writeHead(405, { allow: "POST", "cache-control": "no-store" });
    res.end();
    return;
  }

  try {
    const body = await readJson(req);
    const mcp = createMcpServer();
    const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined });
    res.on("close", () => { void transport.close(); void mcp.close(); });
    await mcp.connect(transport);
    await transport.handleRequest(req, res, body);
  } catch (error) {
    if (!res.headersSent) {
      sendJson(res, 400, { error: "invalid_mcp_request", message: redact((error as Error).message) });
    } else {
      res.end();
    }
  }
});

httpServer.listen(PORT, HOST, () => {
  process.stdout.write(`${NAME} listening on http://${HOST}:${PORT}/mcp\n`);
});

process.on("SIGTERM", () => httpServer.close(() => process.exit(0)));
process.on("SIGINT", () => httpServer.close(() => process.exit(0)));
