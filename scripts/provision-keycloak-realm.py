#!/usr/bin/env python3
"""Idempotently provision the mrcute realm through Keycloak's Admin REST API."""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = os.environ.get("KEYCLOAK_BASE_URL", "https://sso.mrcute.space").rstrip("/")
ADMIN_USERNAME = os.environ["KEYCLOAK_ADMIN_USERNAME"]
ADMIN_PASSWORD = os.environ["KEYCLOAK_ADMIN_PASSWORD"]
REALM_NAME = "mrcute"


def request(path, method="GET", data=None, token=None, expected=(200,)):
    body = None if data is None else json.dumps(data).encode()
    headers = {"Accept": "application/json"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(BASE_URL + path, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            raw = response.read()
            if response.status not in expected:
                raise RuntimeError(f"Unexpected HTTP status {response.status} for {method} {path}")
            return response.status, json.loads(raw) if raw else None
    except urllib.error.HTTPError as exc:
        # Never print response bodies: they may contain sensitive server details.
        if exc.code in expected:
            raw = exc.read()
            return exc.code, json.loads(raw) if raw else None
        if exc.code in (401, 403):
            raise RuntimeError("Keycloak Admin API authentication/authorization failed; verify the production admin credentials and role.") from None
        raise RuntimeError(f"Keycloak Admin API request failed with HTTP {exc.code}: {method} {path}") from None
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(f"Keycloak Admin API is unreachable for {method} {path}: {type(exc).__name__}") from None



TCE_CLIENT_ID = "tce-dashboard"
TCE_CALLBACK = "https://tce.mrcute.space/auth/callback"
TCE_ORIGIN = "https://tce.mrcute.space"
TCE_LOGOUT_REDIRECT = "https://tce.mrcute.space/login"
API_AUDIENCE = "nest-api"
API_AUDIENCE_SCOPE = "nest-api-audience"


def get_client(token, client_id):
    query = urllib.parse.urlencode({"clientId": client_id, "exact": "true"})
    _, clients = request(f"/admin/realms/{REALM_NAME}/clients?{query}", token=token, expected=(200,))
    if not isinstance(clients, list):
        raise RuntimeError(f"Unexpected client list response for {client_id}.")
    matches = [client for client in clients if client.get("clientId") == client_id]
    if len(matches) > 1:
        raise RuntimeError(f"Multiple exact matches found for client {client_id}.")
    return matches[0] if matches else None


def ensure_api_audience_scope(token):
    _, scopes = request(f"/admin/realms/{REALM_NAME}/client-scopes", token=token, expected=(200,))
    if not isinstance(scopes, list):
        raise RuntimeError("Unexpected Keycloak client-scope list response.")
    matches = [scope for scope in scopes if scope.get("name") == API_AUDIENCE_SCOPE]
    if len(matches) > 1:
        raise RuntimeError("Multiple nest-api-audience scopes exist; refusing ambiguous mutation.")
    if matches:
        scope = matches[0]
        scope_id = scope.get("id")
        if not scope_id:
            raise RuntimeError("Existing nest-api-audience scope has no internal ID.")
        _, mappers = request(
            f"/admin/realms/{REALM_NAME}/client-scopes/{scope_id}/protocol-mappers/models",
            token=token,
            expected=(200,),
        )
        valid = any(
            mapper.get("protocolMapper") == "oidc-audience-mapper"
            and mapper.get("config", {}).get("included.client.audience") == API_AUDIENCE
            and mapper.get("config", {}).get("access.token.claim") == "true"
            and mapper.get("config", {}).get("id.token.claim") == "false"
            for mapper in (mappers or [])
        )
        if not valid:
            raise RuntimeError("Existing nest-api-audience scope does not match the expected API audience contract; refusing to modify a potentially shared scope.")
        return scope_id

    scope_body = {
        "name": API_AUDIENCE_SCOPE,
        "description": "Adds the NestJS resource-server audience to access tokens for approved clients.",
        "protocol": "openid-connect",
        "attributes": {
            "include.in.token.scope": "true",
            "display.on.consent.screen": "false",
        },
    }
    request(
        f"/admin/realms/{REALM_NAME}/client-scopes",
        method="POST",
        data=scope_body,
        token=token,
        expected=(201,),
    )
    _, scopes = request(f"/admin/realms/{REALM_NAME}/client-scopes", token=token, expected=(200,))
    matches = [scope for scope in scopes if scope.get("name") == API_AUDIENCE_SCOPE]
    if len(matches) != 1 or not matches[0].get("id"):
        raise RuntimeError("Could not resolve the newly created API audience scope.")
    scope_id = matches[0]["id"]
    mapper = {
        "name": "NestJS API audience",
        "protocol": "openid-connect",
        "protocolMapper": "oidc-audience-mapper",
        "consentRequired": False,
        "config": {
            "included.client.audience": API_AUDIENCE,
            "id.token.claim": "false",
            "access.token.claim": "true",
        },
    }
    request(
        f"/admin/realms/{REALM_NAME}/client-scopes/{scope_id}/protocol-mappers/models",
        method="POST",
        data=mapper,
        token=token,
        expected=(201,),
    )
    return scope_id


def ensure_tce_client(token):
    scope_id = ensure_api_audience_scope(token)
    existing = get_client(token, TCE_CLIENT_ID)
    desired = {
        "clientId": TCE_CLIENT_ID,
        "name": "TCE Dashboard",
        "enabled": True,
        "protocol": "openid-connect",
        "publicClient": True,
        "standardFlowEnabled": True,
        "implicitFlowEnabled": False,
        "directAccessGrantsEnabled": False,
        "serviceAccountsEnabled": False,
        "redirectUris": [TCE_CALLBACK],
        "webOrigins": [TCE_ORIGIN],
        "attributes": {
            "pkce.code.challenge.method": "S256",
            "post.logout.redirect.uris": TCE_LOGOUT_REDIRECT,
        },
    }
    if existing is None:
        request(
            f"/admin/realms/{REALM_NAME}/clients",
            method="POST",
            data=desired,
            token=token,
            expected=(201,),
        )
        existing = get_client(token, TCE_CLIENT_ID)
        if existing is None:
            raise RuntimeError("Keycloak did not return the newly created tce-dashboard client.")
        print("Created tce-dashboard OIDC client.")
    else:
        # Preserve unrelated client attributes and protocol mappers, while
        # enforcing the narrowly defined TCE redirect/security contract.
        merged = dict(existing)
        merged.update(desired)
        attributes = dict(existing.get("attributes") or {})
        attributes.update(desired["attributes"])
        merged["attributes"] = attributes
        request(
            f"/admin/realms/{REALM_NAME}/clients/{existing['id']}",
            method="PUT",
            data=merged,
            token=token,
            expected=(204,),
        )
        print("Updated tce-dashboard OIDC client in place.")

    _, assigned_scopes = request(
        f"/admin/realms/{REALM_NAME}/clients/{existing['id']}/default-client-scopes",
        token=token,
        expected=(200,),
    )
    if not any(scope.get("id") == scope_id or scope.get("name") == API_AUDIENCE_SCOPE for scope in (assigned_scopes or [])):
        request(
            f"/admin/realms/{REALM_NAME}/clients/{existing['id']}/default-client-scopes/{scope_id}",
            method="PUT",
            token=token,
            expected=(204,),
        )

    client = get_client(token, TCE_CLIENT_ID)
    if client is None:
        raise RuntimeError("tce-dashboard client disappeared after provisioning.")
    redirects = client.get("redirectUris") or []
    origins = client.get("webOrigins") or []
    attrs = client.get("attributes") or {}
    checks = {
        "enabled": client.get("enabled") is True,
        "publicClient": client.get("publicClient") is True,
        "standardFlowEnabled": client.get("standardFlowEnabled") is True,
        "implicitFlowEnabled": client.get("implicitFlowEnabled") is False,
        "directAccessGrantsEnabled": client.get("directAccessGrantsEnabled") is False,
        "serviceAccountsEnabled": client.get("serviceAccountsEnabled") is False,
        "exactCallback": redirects == [TCE_CALLBACK],
        "exactWebOrigin": origins == [TCE_ORIGIN],
        "pkceS256": attrs.get("pkce.code.challenge.method") == "S256",
        "exactPostLogoutRedirect": attrs.get("post.logout.redirect.uris") == TCE_LOGOUT_REDIRECT,
    }
    _, assigned_scopes = request(
        f"/admin/realms/{REALM_NAME}/clients/{client['id']}/default-client-scopes",
        token=token,
        expected=(200,),
    )
    checks["apiAudienceScopeAssigned"] = any(
        scope.get("id") == scope_id or scope.get("name") == API_AUDIENCE_SCOPE
        for scope in (assigned_scopes or [])
    )
    failed = [name for name, passed in checks.items() if not passed]
    for name, passed in checks.items():
        print(f"tce_client_{name}={'true' if passed else 'false'}")
    if failed:
        raise RuntimeError("TCE OIDC client verification failed for: " + ", ".join(failed))


def main():
    token_url = BASE_URL + "/realms/master/protocol/openid-connect/token"
    payload = urllib.parse.urlencode({
        "grant_type": "password",
        "client_id": "admin-cli",
        "username": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD,
    }).encode()
    req = urllib.request.Request(token_url, data=payload, headers={"Content-Type": "application/x-www-form-urlencoded"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            token_response = json.loads(response.read())
    except urllib.error.HTTPError as exc:
        if exc.code in (400, 401, 403):
            raise RuntimeError("Could not authenticate to the master realm Admin API. Confirm the configured admin is a persistent admin account and direct access grants are available.") from None
        raise RuntimeError(f"Token endpoint failed with HTTP {exc.code}") from None
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(f"Keycloak token endpoint is unreachable: {type(exc).__name__}") from None

    token = token_response.get("access_token")
    if not token:
        raise RuntimeError("Keycloak token response did not contain an access token.")

    status, existing = request(f"/admin/realms/{REALM_NAME}", token=token, expected=(200, 404))
    # Seed the listener set before either branch so first-time realm creation
    # never references an uninitialized local variable.
    listeners = {"jboss-logging"}
    if status == 404:
        realm = {
            "realm": REALM_NAME,
            "enabled": True,
            "registrationAllowed": True,
            "verifyEmail": False,
            "resetPasswordAllowed": False,
            "loginWithEmailAllowed": True,
            "duplicateEmailsAllowed": False,
            "editUsernameAllowed": False,
            "rememberMe": True,
            "bruteForceProtected": True,
            "eventsEnabled": True,
            "eventsListeners": sorted(listeners),
            "adminEventsEnabled": True,
            "adminEventsDetailsEnabled": False,
            "passwordPolicy": "length(12) and notUsername",
        }
        request("/admin/realms", method="POST", data=realm, token=token, expected=(201,))
        print("Created realm mrcute with self-registration enabled, email verification disabled, and security events enabled.")
    else:
        # Preserve existing clients and unrelated realm settings.
        listeners.update(existing.get("eventsListeners") or [])
        existing.update({
            "enabled": True,
            "registrationAllowed": True,
            "verifyEmail": False,
            "resetPasswordAllowed": False,
            "loginWithEmailAllowed": True,
            "duplicateEmailsAllowed": False,
            "editUsernameAllowed": False,
            "rememberMe": True,
            "bruteForceProtected": True,
            "eventsEnabled": True,
            "eventsListeners": sorted(listeners),
            "adminEventsEnabled": True,
            "adminEventsDetailsEnabled": False,
            "passwordPolicy": "length(12) and notUsername",
        })
        request(f"/admin/realms/{REALM_NAME}", method="PUT", data=existing, token=token, expected=(204,))
        print("Updated realm mrcute in place; existing clients and unrelated realm settings were preserved.")

    _, verified = request(f"/admin/realms/{REALM_NAME}", token=token, expected=(200,))
    checks = {
        "enabled": verified.get("enabled") is True,
        "registrationAllowed": verified.get("registrationAllowed") is True,
        "verifyEmail": verified.get("verifyEmail") is False,
        "resetPasswordAllowed": verified.get("resetPasswordAllowed") is False,
        "bruteForceProtected": verified.get("bruteForceProtected") is True,
        "eventsEnabled": verified.get("eventsEnabled") is True,
    }
    failed = [key for key, passed in checks.items() if not passed]
    if failed:
        raise RuntimeError("Realm policy verification failed for: " + ", ".join(failed))
    _, master = request("/admin/realms/master", token=token, expected=(200,))
    if master.get("registrationAllowed") is True:
        raise RuntimeError("Safety check failed: self-registration is enabled on master; refusing to report success.")
    print("Verified realm policy; master realm remains registration-disabled.")

    # Provision only the TCE client and its dedicated API-audience scope. Do not
    # import a full realm export or alter other clients/roles.
    ensure_tce_client(token)
    print("Provisioned and verified the tce-dashboard public OIDC client contract.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"::error::{exc}", file=sys.stderr)
        sys.exit(1)
