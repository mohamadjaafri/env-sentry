import re

SUSPECT_KEYS = [
    "SECRET", "TOKEN", "KEY", "PASSWORD", "CLIENT_SECRET", "PRIVATE"
]

def scan_env_file(filepath):
    findings = []
    try:
        with open(filepath, "r") as file:
            for lineno, line in enumerate(file, start=1):
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue

                key, value = map(str.strip, line.split("=", 1))

                if is_suspect_key(key) or is_suspect_value(value):
                    findings.append((lineno, key, value))

    except FileNotFoundError:
        print(f"❌ File not found: {filepath}")
    except Exception as e:
        print(f"❌ Error reading file: {e}")

    return findings

def is_suspect_key(key):
    return any(k in key.upper() for k in SUSPECT_KEYS)

def is_suspect_value(value):
    # Heuristics for secret-looking values
    if len(value) > 40 and re.fullmatch(r"[A-Za-z0-9+/=]+", value):  # base64
        return True
    if len(value) > 32 and re.fullmatch(r"[A-Fa-f0-9]+", value):     # hex
        return True
    return False