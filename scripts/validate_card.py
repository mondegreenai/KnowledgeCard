#!/usr/bin/env python3
"""
Validate a Knowledge Card against the Knowledge Card JSON Schema.

Usage:
    python scripts/validate_card.py examples/wind-energy-gearbox-spalling.jsonld

Requires:
    pip install jsonschema

Copyright (c) 2026 Mondegreen.ai. Licensed under Apache-2.0.
"""

import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:
    sys.exit("This script requires 'jsonschema'. Install it with: pip install jsonschema")

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = REPO_ROOT / "schema" / "knowledge-card.schema.json"


def load_json(path: Path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def main(argv):
    if len(argv) != 2:
        sys.exit("Usage: python scripts/validate_card.py <card.jsonld>")

    card_path = Path(argv[1])
    schema = load_json(SCHEMA_PATH)
    card = load_json(card_path)

    validator = Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(card), key=lambda e: e.path)

    if not errors:
        print(f"OK: {card_path.name} is a valid Knowledge Card.")
        return 0

    print(f"INVALID: {card_path.name} has {len(errors)} error(s):\n")
    for err in errors:
        location = "/".join(str(p) for p in err.path) or "(root)"
        print(f"  at {location}: {err.message}")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
