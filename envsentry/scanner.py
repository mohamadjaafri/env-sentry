"""Heuristic detection of likely secrets in dotenv files."""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass
from pathlib import Path

PathLike = str | Path

SUSPECT_KEY_PARTS = (
    "SECRET",
    "TOKEN",
    "PASSWORD",
    "PASSWD",
    "PRIVATE_KEY",
    "API_KEY",
    "ACCESS_KEY",
    "CLIENT_KEY",
)

_BASE64_RE = re.compile(r"^[A-Za-z0-9+/]+={0,2}$")
_HEX_RE = re.compile(r"^[A-Fa-f0-9]+$")
_PLACEHOLDERS = {
    "",
    "changeme",
    "change-me",
    "replace-me",
    "your-value",
    "your-secret",
    "example",
    "placeholder",
}


@dataclass(frozen=True)
class Finding:
    """A redacted finding. Secret values are deliberately never retained."""

    file: str
    line: int
    key: str
    reason: str

    def to_dict(self) -> dict[str, object]:
        """Return a JSON-serializable representation."""
        return asdict(self)


def is_suspect_key(key: str) -> bool:
    """Return whether a variable name indicates sensitive material."""
    normalized = key.upper()
    return any(part in normalized for part in SUSPECT_KEY_PARTS)


def _normalize_value(raw_value: str) -> str:
    value = raw_value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]
    elif " #" in value:
        value = value.split(" #", 1)[0].rstrip()
    return value.strip()


def _is_placeholder(value: str) -> bool:
    return value.lower() in _PLACEHOLDERS or value.startswith(("$", "${"))


def value_detection_reason(value: str) -> str | None:
    """Return a reason for suspicious value shapes without returning the value."""
    candidate = _normalize_value(value)
    if _is_placeholder(candidate):
        return None
    if len(candidate) > 40 and _BASE64_RE.fullmatch(candidate):
        return "long base64-like value"
    if len(candidate) > 32 and _HEX_RE.fullmatch(candidate):
        return "long hexadecimal value"
    return None


def is_suspect_value(value: str) -> bool:
    """Return whether a value matches one of the supported heuristics."""
    return value_detection_reason(value) is not None


def scan_env_file(filepath: PathLike) -> list[Finding]:
    """Scan a dotenv file and return redacted findings.

    The scanner intentionally uses simple dotenv parsing. It does not execute
    shell expressions, expand variables, or follow references to external files.
    """
    path = Path(filepath)
    findings: list[Finding] = []

    with path.open("r", encoding="utf-8") as env_file:
        for line_number, raw_line in enumerate(env_file, start=1):
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("export "):
                line = line[len("export ") :].lstrip()
            if "=" not in line:
                continue

            key, raw_value = line.split("=", 1)
            key = key.strip()
            value = _normalize_value(raw_value)
            if not key or _is_placeholder(value):
                continue

            reasons: list[str] = []
            if is_suspect_key(key):
                reasons.append("sensitive-looking variable name")
            value_reason = value_detection_reason(value)
            if value_reason:
                reasons.append(value_reason)

            if reasons:
                findings.append(
                    Finding(
                        file=str(path),
                        line=line_number,
                        key=key,
                        reason=", ".join(reasons),
                    )
                )

    return findings
