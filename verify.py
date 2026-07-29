#!/usr/bin/env python3
"""Verify an NL;NL Labs commitment file against a locally recomputed hash.

Usage:
    python3 verify.py path/to/battery_v2.json
    python3 verify.py path/to/or_gateway_probes_v1.json <expected sha256>

There are two kinds of commitment, hashed two different ways. This script
picks the recipe by looking at the shape of the file, and prints which one it
used.

1. canonical items — a battery or sensor file (it has an "items" array).
   This reimplements, byte-for-byte, the canonicalisation used by the NL;NL
   Labs meter (functions canonical_items_json / battery_hash in meter_lib.py):

     - keep exactly 7 fields per item: id, family, class_label, prompt,
       answer (coerced to str), answer_type, params
     - sort items by id
     - json.dumps(..., sort_keys=True, ensure_ascii=False,
       separators=(",", ":"))
     - encode utf-8, sha256, hexdigest

   The committed hash travels inside the file, in "battery_hash".

2. whole file bytes — the gateway probe set (it has a "probes" array). The
   meter hashes the raw bytes of the file itself: sha256(file bytes). Such a
   file cannot carry its own hash, because writing the hash into it would
   change the bytes. So the expected hash must be passed as a second
   argument. Take it from the published commitment record, not from this
   script: a verifier that ships with the answer inside it proves nothing.

Any other shape is refused, not guessed at.

This prints only the recipe used, the two hashes, and a MATCH/MISMATCH
verdict. It never prints any item content (no prompts, answers, ids, or
params).
"""

import hashlib
import json
import sys

USAGE = (
    "Usage:\n"
    "  python3 verify.py path/to/battery_v2.json\n"
    "  python3 verify.py path/to/or_gateway_probes_v1.json <expected sha256>"
)


def canonical_items_json(items):
    core = [
        {
            "id": it["id"],
            "family": it["family"],
            "class_label": it["class_label"],
            "prompt": it["prompt"],
            "answer": str(it["answer"]),
            "answer_type": it["answer_type"],
            "params": it["params"],
        }
        for it in items
    ]
    core.sort(key=lambda x: x["id"])
    return json.dumps(core, sort_keys=True, ensure_ascii=False, separators=(",", ":"))


def battery_hash(items):
    return hashlib.sha256(canonical_items_json(items).encode("utf-8")).hexdigest()


def file_hash(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def main():
    if len(sys.argv) not in (2, 3):
        print(USAGE, file=sys.stderr)
        return 2

    path = sys.argv[1]
    expected = sys.argv[2] if len(sys.argv) == 3 else None

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict) and "items" in data:
        recipe = "canonical items (expected hash read from the file's battery_hash)"
        computed = battery_hash(data["items"])
        stored = data.get("battery_hash", "<missing>")
    elif isinstance(data, dict) and "probes" in data:
        recipe = "whole file bytes (expected hash given on the command line)"
        if expected is None:
            print(
                "This is a probe set. Its commitment is the sha256 of the whole "
                "file, which the file cannot carry. Pass the expected hash as a "
                "second argument.",
                file=sys.stderr,
            )
            return 2
        computed = file_hash(path)
        stored = expected
    else:
        print(
            f"{path} is not a recognised commitment file: expected a top-level "
            '"items" array (battery or sensor) or "probes" array (gateway probe '
            "set).",
            file=sys.stderr,
        )
        return 2

    print(f"recipe:        {recipe}")
    print(f"computed hash: {computed}")
    print(f"stored hash:   {stored}")

    if computed == stored:
        print("MATCH")
        return 0
    else:
        print("MISMATCH")
        return 1


if __name__ == "__main__":
    sys.exit(main())
