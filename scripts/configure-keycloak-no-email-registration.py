#!/usr/bin/env python3
"""Enable Keycloak self-registration without email verification for the mrcute realm.

This deliberately does not provision application accounts or weaken TCE's OIDC
email_verified / ACTIVE-account checks.
"""
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE_URL = os.environ.get("KEYCLOAK_BASE_URL", "https://sso.mrcute.space").rstrip("/")
REALM = "mrcute"
ADMIN_USERNAME = os.environ["KEYCLOAK_ADMIN_USERNAME"]
ADMIN_PASSWORD = os.environ["KEYCLOAK_ADMIN_PASSWORD"]


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
        if exc.code in (401, 403):
            raise RuntimeError("Keycloak Admin API authentication/authorization failed; verify production admin credentials and role.") from None
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
    req = urllib.request.Request(
        token_url, data=payload,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            token_response = json.loads(response.read())
    except urllib.error.HTTPError as exc:
        if exc.code in (400, 401, 403):
            raise RuntimeError("Could not authenticate to the master realm Admin API; verify the configured admin account.") from None
        raise RuntimeError(f"Keycloak token endpoint failed with HTTP {exc.code}") from None
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(f"Keycloak token endpoint is unreachable: {type(exc).__name__}") from None

    token = token_response.get("access_token")
    if not token:
        raise RuntimeError("Keycloak token response did not contain an access token.")

    _, realm = request(f"/admin/realms/{REALM}", token=token, expected=(200,))
    if realm.get("enabled") is not True:
        raise RuntimeError("The mrcute realm is disabled; refusing to change registration settings.")

    realm.update({
        "registrationAllowed": True,
        "verifyEmail": False,
        "resetPasswordAllowed": False,
        "loginWithEmailAllowed": True,
        "duplicateEmailsAllowed": False,
        "bruteForceProtected": True,
    })
    request(f"/admin/realms/{REALM}", method="PUT", data=realm, token=token, expected=(204,))

    _, verified = request(f"/admin/realms/{REALM}", token=token, expected=(200,))
    checks = {
        "registrationAllowed": verified.get("registrationAllowed") is True,
        "verifyEmail": verified.get("verifyEmail") is False,
        "resetPasswordAllowed": verified.get("resetPasswordAllowed") is False,
        "loginWithEmailAllowed": verified.get("loginWithEmailAllowed") is True,
        "duplicateEmailsAllowed": verified.get("duplicateEmailsAllowed") is False,
        "bruteForceProtected": verified.get("bruteForceProtected") is True,
    }
    for key, passed in checks.items():
        print(f"keycloak_no_email_{key}={'true' if passed else 'false'}")
    failed = [key for key, passed in checks.items() if not passed]
    if failed:
        raise RuntimeError("Keycloak registration configuration verification failed for: " + ", ".join(failed))

    _, master = request("/admin/realms/master", token=token, expected=(200,))
    if master.get("registrationAllowed") is True:
        raise RuntimeError("Safety check failed: registration is enabled on the master realm.")
    print("mrcute self-registration enabled without email verification.")
    print("Password reset remains disabled; master realm registration remains unchanged.")
    print("This does not bypass TCE's verified-email and existing ACTIVE-account checks.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"::error::{exc}", file=sys.stderr)
        sys.exit(1)
