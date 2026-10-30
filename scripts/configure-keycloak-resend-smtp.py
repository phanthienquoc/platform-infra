#!/usr/bin/env python3
"""Configure Resend SMTP for the mrcute realm and enable verified registration."""
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
SMTP_API_KEY = os.environ["RESEND_SMTP_API_KEY"]
SMTP_FROM = os.environ["RESEND_SMTP_FROM"]
SMTP_FROM_DISPLAY_NAME = os.environ.get("RESEND_SMTP_FROM_DISPLAY_NAME", "mrcute SSO")


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
    if not SMTP_FROM or "@" not in SMTP_FROM:
        raise RuntimeError("RESEND_SMTP_FROM must be a verified sender email address.")
    if not SMTP_API_KEY:
        raise RuntimeError("Missing RESEND_SMTP_API_KEY.")

    token_url = BASE_URL + "/realms/master/protocol/openid-connect/token"
    payload = urllib.parse.urlencode({
        "grant_type": "password",
        "client_id": "admin-cli",
        "username": ADMIN_USERNAME,
        "password": ADMIN_PASSWORD,
    }).encode()
    req = urllib.request.Request(
        token_url,
        data=payload,
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
        raise RuntimeError("The mrcute realm is disabled; refusing to enable public registration implicitly.")

    smtp = {
        "host": "smtp.resend.com",
        "port": "465",
        "from": SMTP_FROM,
        "fromDisplayName": SMTP_FROM_DISPLAY_NAME,
        "auth": "true",
        "user": "resend",
        "password": SMTP_API_KEY,
        "ssl": "true",
        "starttls": "false",
    }

    # Test the connection before changing the live realm's registration policy.
    request(
        f"/admin/realms/{REALM}/testSMTPConnection",
        method="POST",
        data=smtp,
        token=token,
        expected=(200, 204),
    )
    print("Resend SMTP connection test passed.")

    realm["smtpServer"] = smtp
    realm.update({
        "registrationAllowed": True,
        "verifyEmail": True,
        "resetPasswordAllowed": True,
        "loginWithEmailAllowed": True,
        "duplicateEmailsAllowed": False,
        "bruteForceProtected": True,
    })
    request(f"/admin/realms/{REALM}", method="PUT", data=realm, token=token, expected=(204,))

    _, verified = request(f"/admin/realms/{REALM}", token=token, expected=(200,))
    actual_smtp = verified.get("smtpServer") or {}
    checks = {
        "registrationAllowed": verified.get("registrationAllowed") is True,
        "verifyEmail": verified.get("verifyEmail") is True,
        "resetPasswordAllowed": verified.get("resetPasswordAllowed") is True,
        "smtpHost": actual_smtp.get("host") == "smtp.resend.com",
        "smtpPort": str(actual_smtp.get("port")) == "465",
        "smtpFrom": actual_smtp.get("from") == SMTP_FROM,
        "smtpAuth": str(actual_smtp.get("auth")).lower() == "true",
        "smtpSsl": str(actual_smtp.get("ssl")).lower() == "true",
    }
    for key, passed in checks.items():
        print(f"keycloak_email_{key}={'true' if passed else 'false'}")
    failed = [key for key, passed in checks.items() if not passed]
    if failed:
        raise RuntimeError("Keycloak email configuration verification failed for: " + ", ".join(failed))

    _, master = request("/admin/realms/master", token=token, expected=(200,))
    if master.get("registrationAllowed") is True:
        raise RuntimeError("Safety check failed: registration is enabled on the master realm.")
    print("Resend SMTP configured; mrcute registration requires email verification; password reset is enabled.")
    print("Master realm registration remains unchanged and is not enabled by this workflow.")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"::error::{exc}", file=sys.stderr)
        sys.exit(1)
