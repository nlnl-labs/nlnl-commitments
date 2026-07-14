#!/usr/bin/env python3
"""Verify a battery file's battery_hash against a locally recomputed hash.

Usage:
    python3 verify.py path/to/battery_v2.json

This reimplements, byte-for-byte, the canonicalisation in
nlnl/meter/meter_lib.py (functions canonical_items_json / battery_hash):

  - keep exactly 7 fields per item: id, family, class_label, prompt,
    answer (coerced to str), answer_type, params
  - sort items by id
  - json.dumps(..., sort_keys=True, ensure_ascii=False,
    separators=(",", ":"))
  - encode utf-8, sha256, hexdigest

It prints only the two hashes and a MATCH/MISMATCH verdict. It never prints
any item content (no prompts, answers, ids, or params).
"""

import hashlib
import json
import sys


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


def main():
    if len(sys.argv) != 2:
        print("Usage: python3 verify.py path/to/battery_v2.json", file=sys.stderr)
        return 2

    path = sys.argv[1]
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    computed = battery_hash(data["items"])
    stored = data.get("battery_hash", "<missing>")

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
