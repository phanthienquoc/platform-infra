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
            "eventsListeners": ["jboss-logging"],
            "adminEventsEnabled": True,
            "adminEventsDetailsEnabled": False,
            "passwordPolicy": "length(12) and notUsername",
        }
        request("/admin/realms", method="POST", data=realm, token=token, expected=(201,))
        print("Created realm mrcute with self-registration enabled, email verification disabled, and security events enabled.")
    else:
        # Preserve existing clients and unrelated realm settings.
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
            "eventsListeners": ["jboss-logging"],
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
    print("No app-specific OIDC clients or application roles were created.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"::error::{exc}", file=sys.stderr)
        sys.exit(1)
