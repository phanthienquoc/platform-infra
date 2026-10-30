#!/usr/bin/env python3
"""Validate the declarative SSO app registry without external dependencies."""
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "config" / "sso" / "apps"
APP_ID = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
CLIENT_ID = re.compile(r"^[a-zA-Z0-9._:-]{1,100}$")
REPOSITORY = re.compile(r"^phanthienquoc/[A-Za-z0-9_.-]+$")
AUDIENCE = re.compile(r"^[a-zA-Z0-9._:-]{1,100}$")
REQUIRED = {
    "app_id", "repository", "enabled", "client_id", "client_type",
    "redirect_uris", "web_origins", "post_logout_redirect_uris", "api_audience",
}


def fail(message):
    raise ValueError(message)


def validate_url(value, field, allow_path=True):
    if not isinstance(value, str) or "*" in value or not value:
        fail(f"{field}: expected a non-empty exact URL; wildcards are forbidden")
    parsed = urlsplit(value)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        fail(f"{field}: must be an HTTPS URL without embedded credentials")
    if parsed.query or parsed.fragment:
        fail(f"{field}: query strings and fragments are not allowed")
    host = parsed.hostname.lower()
    if host != "mrcute.space" and not host.endswith(".mrcute.space"):
        fail(f"{field}: hostname must be mrcute.space or a subdomain of it")
    if not allow_path and parsed.path not in ("", "/"):
        fail(f"{field}: web origin must not include a path")
    if parsed.port not in (None, 443):
        fail(f"{field}: non-standard ports are forbidden")
    return value


def load_manifest(path):
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        fail(f"{path}: manifest root must be an object")
    missing = REQUIRED - data.keys()
    extra = data.keys() - REQUIRED
    if missing:
        fail(f"{path}: missing fields: {', '.join(sorted(missing))}")
    if extra:
        fail(f"{path}: unknown fields: {', '.join(sorted(extra))}")
    if not APP_ID.fullmatch(str(data["app_id"])) or path.stem != data["app_id"]:
        fail(f"{path}: app_id must be lowercase kebab-case and match the filename")
    if not REPOSITORY.fullmatch(str(data["repository"])):
        fail(f"{path}: repository must be an explicit phanthienquoc/<repo> name")
    if data["client_type"] != "public-pkce":
        fail(f"{path}: only public-pkce browser clients are supported")
    if not isinstance(data["enabled"], bool):
        fail(f"{path}: enabled must be a boolean")
    if not CLIENT_ID.fullmatch(str(data["client_id"])):
        fail(f"{path}: invalid client_id")
    if not AUDIENCE.fullmatch(str(data["api_audience"])):
        fail(f"{path}: invalid api_audience")
    for field in ("redirect_uris", "web_origins", "post_logout_redirect_uris"):
        values = data[field]
        if not isinstance(values, list) or not values or any(not isinstance(x, str) for x in values):
            fail(f"{path}: {field} must be a non-empty list of exact URLs")
        if len(values) != len(set(values)):
            fail(f"{path}: {field} contains duplicates")
        for value in values:
            validate_url(value, field, allow_path=(field != "web_origins"))
    if any(urlsplit(value).path not in ("", "/") for value in data["web_origins"]):
        fail(f"{path}: web_origins entries must be origins without paths")
    callback_hosts = {urlsplit(value).hostname for value in data["redirect_uris"]}
    origin_hosts = {urlsplit(value).hostname for value in data["web_origins"]}
    if not callback_hosts.issubset(origin_hosts):
        fail(f"{path}: every redirect URI hostname must have an explicit web origin")
    return data


def main():
    targets = [ROOT / arg for arg in sys.argv[1:]] if len(sys.argv) > 1 else sorted(REGISTRY.glob("*.json"))
    if not targets:
        fail(f"No SSO app manifests found in {REGISTRY}")
    manifests = [load_manifest(path) for path in targets]
    seen = {}
    for key in ("app_id", "client_id", "repository"):
        for manifest in manifests:
            value = manifest[key].lower() if key == "repository" else manifest[key]
            if value in seen.setdefault(key, set()):
                fail(f"Duplicate {key}: {manifest[key]}")
            seen[key].add(value)
    print(f"sso_registry_valid=true manifests={len(manifests)}")
    for manifest in manifests:
        print(f"validated_app={manifest['app_id']} repository={manifest['repository']}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        print(f"::error::{exc}", file=sys.stderr)
        sys.exit(1)
