import crypto from "node:crypto";
import express from "express";

const app = express();
app.disable("x-powered-by");
app.use(express.json({ limit: "32kb" }));

const cookieName = process.env.AUTH_COOKIE_NAME || "__Host-microfe_session";
function reqId(req) { return req.get("x-request-id") || crypto.randomUUID(); }

app.use((req, res, next) => {
  res.setHeader("x-request-id", reqId(req));
  next();
});

app.get("/health", (_req, res) => res.json({ ok: true, service: "microfe-auth" }));

app.get("/auth/me", (req, res) => {
  const authenticated = Boolean(req.headers.cookie?.includes(cookieName + "="));
  if (!authenticated) {
    return res.status(401).json({ code: "AUTH_REQUIRED", message: "Authentication required", requestId: res.getHeader("x-request-id") });
  }
  return res.json({ authenticated: true });
});

app.post("/auth/logout", (_req, res) => {
  res.setHeader("Set-Cookie", cookieName + "=; Max-Age=0; Path=/; HttpOnly; Secure; SameSite=Lax");
  res.status(204).end();
});

export { app };

if (process.env.NODE_ENV !== "test") {
  const port = Number(process.env.PORT || 3000);
  app.listen(port, "0.0.0.0", () => console.log("microfe-auth listening on :" + port));
}