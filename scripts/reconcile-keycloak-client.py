#!/usr/bin/env python3
"""Idempotently reconcile one reviewed SSO app manifest to the Keycloak mrcute realm."""
import argparse
import importlib.util
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("sso_registry_validator", ROOT / "scripts" / "validate-sso-registry.py")
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)

BASE_URL = os.environ.get("KEYCLOAK_BASE_URL", "https://sso.mrcute.space").rstrip("/")
REALM = "mrcute"
TIMEOUT = 20


def request(path, method="GET", data=None, token=None, expected=(200,)):
    body = None if data is None else json.dumps(data).encode()
    headers = {"Accept": "application/json"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(BASE_URL + path, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            raw = response.read()
            if response.status not in expected:
                raise RuntimeError(f"Unexpected HTTP {response.status} for {method} {path}")
            return response.status, json.loads(raw) if raw else None
    except urllib.error.HTTPError as exc:
        if exc.code in expected:
            raw = exc.read()
            return exc.code, json.loads(raw) if raw else None
        if exc.code in (401, 403):
            raise RuntimeError("Keycloak Admin API rejected credentials or permissions.") from None
        raise RuntimeError(f"Keycloak Admin API returned HTTP {exc.code} for {method} {path}") from None
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(f"Keycloak Admin API unavailable ({type(exc).__name__}).") from None


def get_client(token, client_id):
    query = urllib.parse.urlencode({"clientId": client_id, "exact": "true"})
    _, clients = request(f"/admin/realms/{REALM}/clients?{query}", token=token)
    matches = [item for item in (clients or []) if item.get("clientId") == client_id]
    if len(matches) > 1:
        raise RuntimeError(f"Ambiguous exact Keycloak client matches for {client_id}; refusing mutation.")
    return matches[0] if matches else None


def desired_client(manifest):
    return {
        "clientId": manifest["client_id"],
        "name": manifest["app_id"],
        "enabled": manifest["enabled"],
        "protocol": "openid-connect",
        "clientAuthenticatorType": "client-secret",
        "publicClient": True,
        "standardFlowEnabled": True,
        "implicitFlowEnabled": False,
        "directAccessGrantsEnabled": False,
        "serviceAccountsEnabled": False,
        "redirectUris": sorted(manifest["redirect_uris"]),
        "webOrigins": sorted(manifest["web_origins"]),
        "attributes": {
            "pkce.code.challenge.method": "S256",
            "post.logout.redirect.uris": manifest["post_logout_redirect_uris"][0],
        },
    }


def ensure_audience_mapper(token, internal_id, audience):
    _, mappers = request(f"/admin/realms/{REALM}/clients/{internal_id}/protocol-mappers/models", token=token)
    matches = [m for m in (mappers or []) if m.get("name") == "platform-api-audience"]
    if len(matches) > 1:
        raise RuntimeError("Multiple platform-api-audience mappers found; refusing ambiguous mutation.")
    mapper = {
        "name": "platform-api-audience",
        "protocol": "openid-connect",
        "protocolMapper": "oidc-audience-mapper",
        "consentRequired": False,
        "config": {
            "included.client.audience": audience,
            "id.token.claim": "false",
            "access.token.claim": "true",
        },
    }
    if matches:
        config = matches[0].get("config") or {}
        if config.get("included.client.audience") == audience and config.get("access.token.claim") == "true" and config.get("id.token.claim") == "false":
            return
        request(f"/admin/realms/{REALM}/clients/{internal_id}/protocol-mappers/models/{matches[0]['id']}", method="PUT", data=mapper, token=token, expected=(204,))
    else:
        request(f"/admin/realms/{REALM}/clients/{internal_id}/protocol-mappers/models", method="POST", data=mapper, token=token, expected=(201,))


def verify_client(token, manifest):
    client = get_client(token, manifest["client_id"])
    if not client:
        raise RuntimeError("Client is missing after reconciliation.")
    attrs = client.get("attributes") or {}
    checks = {
        "enabled": client.get("enabled") is manifest["enabled"],
        "public_client": client.get("publicClient") is True,
        "standard_flow": client.get("standardFlowEnabled") is True,
        "implicit_flow_disabled": client.get("implicitFlowEnabled") is False,
        "direct_grants_disabled": client.get("directAccessGrantsEnabled") is False,
        "service_accounts_disabled": client.get("serviceAccountsEnabled") is False,
        "exact_redirect_uris": sorted(client.get("redirectUris") or []) == sorted(manifest["redirect_uris"]),
        "exact_web_origins": sorted(client.get("webOrigins") or []) == sorted(manifest["web_origins"]),
        "pkce_s256": attrs.get("pkce.code.challenge.method") == "S256",
        "exact_post_logout_redirects": attrs.get("post.logout.redirect.uris") == manifest["post_logout_redirect_uris"][0],
    }
    _, mappers = request(f"/admin/realms/{REALM}/clients/{client['id']}/protocol-mappers/models", token=token)
    checks["api_audience_access_token_only"] = any(
        mapper.get("name") == "platform-api-audience"
        and mapper.get("protocolMapper") == "oidc-audience-mapper"
        and (mapper.get("config") or {}).get("included.client.audience") == manifest["api_audience"]
        and (mapper.get("config") or {}).get("access.token.claim") == "true"
        and (mapper.get("config") or {}).get("id.token.claim") == "false"
        for mapper in (mappers or [])
    )
    for key, passed in checks.items():
        print(f"{key}={'true' if passed else 'false'}")
    if not all(checks.values()):
        raise RuntimeError("Client contract verification failed.")
    print("client_contract_valid=true")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    manifest_path = Path(args.manifest)
    if not manifest_path.is_absolute():
        manifest_path = ROOT / manifest_path
    manifest = VALIDATOR.load_manifest(manifest_path)
    desired = desired_client(manifest)
    if args.dry_run:
        print(json.dumps({"realm": REALM, "client": desired, "api_audience": manifest["api_audience"]}, indent=2))
        print("dry_run=true no Keycloak requests made")
        return
    username = os.environ.get("KEYCLOAK_ADMIN_USERNAME")
    password = os.environ.get("KEYCLOAK_ADMIN_PASSWORD")
    if not username or not password:
        raise RuntimeError("KEYCLOAK_ADMIN_USERNAME and KEYCLOAK_ADMIN_PASSWORD are required for apply.")
    token_payload = urllib.parse.urlencode({
        "grant_type": "password", "client_id": "admin-cli",
        "username": username, "password": password,
    }).encode()
    req = urllib.request.Request(
        f"{BASE_URL}/realms/master/protocol/openid-connect/token",
        data=token_payload,
        headers={"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
            token_data = json.loads(response.read())
    except urllib.error.HTTPError as exc:
        if exc.code in (400, 401, 403):
            raise RuntimeError("Could not authenticate to Keycloak Admin API; verify protected credentials and role.") from None
        raise RuntimeError(f"Keycloak token endpoint returned HTTP {exc.code}.") from None
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(f"Keycloak token endpoint unavailable ({type(exc).__name__}).") from None
    token = token_data.get("access_token")
    if not token:
        raise RuntimeError("Keycloak token endpoint returned no access token.")
    status, _ = request(f"/admin/realms/{REALM}", token=token, expected=(200, 404))
    if status != 200:
        raise RuntimeError("Target realm mrcute does not exist; refusing to create or modify realm policy.")
    existing = get_client(token, manifest["client_id"])
    if existing is None:
        request(f"/admin/realms/{REALM}/clients", method="POST", data=desired, token=token, expected=(201,))
        existing = get_client(token, manifest["client_id"])
        if existing is None:
            raise RuntimeError("Created client could not be resolved.")
        print(f"client_created={manifest['client_id']}")
    else:
        merged = dict(existing)
        merged.update(desired)
        attrs = dict(existing.get("attributes") or {})
        attrs.update(desired["attributes"])
        merged["attributes"] = attrs
        request(f"/admin/realms/{REALM}/clients/{existing['id']}", method="PUT", data=merged, token=token, expected=(204,))
        print(f"client_updated={manifest['client_id']}")
    ensure_audience_mapper(token, existing["id"], manifest["api_audience"])
    verify_client(token, manifest)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"::error::{exc}", file=sys.stderr)
        sys.exit(1)
