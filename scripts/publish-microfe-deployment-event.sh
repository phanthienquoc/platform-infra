#!/usr/bin/env bash
set -euo pipefail
EVENT=${1:?event}
APP=${2:?app}
VERSION=${3:-unknown}
STATUS=${4:-}
PORT=18080
cleanup(){ [[ -n "${PF_PID:-}" ]] && kill "$PF_PID" >/dev/null 2>&1 || true; }
trap cleanup EXIT
sudo /usr/local/sbin/platform-kubectl -n microfe-platform port-forward svc/microfe-ws "$PORT:8080" >/tmp/microfe-ws-port-forward.log 2>&1 &
PF_PID=$!
for _ in {1..20}; do
  curl -fsS "http://127.0.0.1:$PORT/health" >/dev/null 2>&1 && break
  sleep 1
done
curl --fail-with-body -sS -X POST "http://127.0.0.1:$PORT/internal/events"   -H 'content-type: application/json'   --data "$(python3 - "$EVENT" "$APP" "$VERSION" "$STATUS" <<'PY'
import json,sys,uuid,datetime
event,app,version,status=sys.argv[1:]
print(json.dumps({"id":str(uuid.uuid4()),"channel":"platform.deployments","event":event,
"timestamp":datetime.datetime.now(datetime.timezone.utc).isoformat(),
"data":{"app":app,"version":version,"status":status}}))
PY
)"
