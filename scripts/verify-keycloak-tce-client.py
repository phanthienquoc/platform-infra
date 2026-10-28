#!/usr/bin/env python3
"""Read-only verification of the live Keycloak OIDC client used by TCE."""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = os.environ.get("KEYCLOAK_BASE_URL", "https://sso.mrcute.space").rstrip("/")
ADMIN_USERNAME = os.environ["KEYCLOAK_ADMIN_USERNAME"]
ADMIN_PASSWORD = os.environ["KEYCLOAK_ADMIN_PASSWORD"]
REALM = "mrcute"
CLIENT_ID = "tce-dashboard"
CALLBACK = "https://tce.mrcute.space/auth/callback"
ORIGIN = "https://tce.mrcute.space"


def fail(message):
    print(f"::error::{message}", file=sys.stderr)
    sys.exit(1)


def request(url, data=None, token=None):
    headers = {"Accept": "application/json"}
    if data is not None:
        headers["Content-Type"] = "application/x-www-form-urlencoded"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(url, data=data, headers=headers, method="POST" if data is not None else "GET")
    try:
        with urllib.request.urlopen(req, timeout=15) as response:
            raw = response.read()
            return json.loads(raw) if raw else None
    except urllib.error.HTTPError as exc:
        if exc.code in (401, 403):
            fail("Keycloak Admin API rejected the configured admin credentials/permissions.")
        fail(f"Keycloak Admin API returned HTTP {exc.code} during read-only client verification.")
    except (urllib.error.URLError, TimeoutError):
        fail("Keycloak Admin API was unreachable during read-only client verification.")


def main():
    token_data = urllib.parse.urlencode({
        "grant_type": "password",
        "client_id": "admin-cli",
        "username": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD,
    }).encode()
    token_response = request(f"{BASE_URL}/realms/master/protocol/openid-connect/token", token_data)
    token = token_response.get("access_token") if isinstance(token_response, dict) else None
    if not token:
        fail("Keycloak master realm did not return an admin access token.")

    query = urllib.parse.urlencode({"clientId": CLIENT_ID, "exact": "true"})
    clients = request(f"{BASE_URL}/admin/realms/{REALM}/clients?{query}", token=token)
    if not isinstance(clients, list) or not clients:
        print("client_present=false")
        print("tce_sso_ready=false")
        fail("Realm mrcute exists, but the live tce-dashboard OIDC client was not found.")

    client = clients[0]
    redirects = client.get("redirectUris") or []
    origins = client.get("webOrigins") or []
    attributes = client.get("attributes") or {}
    checks = {
        "client_present": client.get("clientId") == CLIENT_ID,
        "public_client": client.get("publicClient") is True,
        "standard_flow_enabled": client.get("standardFlowEnabled") is True,
        "direct_grants_disabled": client.get("directAccessGrantsEnabled") is False,
        "callback_allowed": CALLBACK in redirects or "https://tce.mrcute.space/*" in redirects,
        "web_origin_allowed": ORIGIN in origins or "+" in origins,
        "pkce_s256": attributes.get("pkce.code.challenge.method") == "S256",
    }
    for name, passed in checks.items():
        print(f"{name}={'true' if passed else 'false'}")
    if not all(checks.values()):
        print("tce_sso_ready=false")
        fail("The live tce-dashboard OIDC client exists but does not meet the expected TCE SSO security contract.")
    print("tce_sso_ready=true")


if __name__ == "__main__":
    main()
