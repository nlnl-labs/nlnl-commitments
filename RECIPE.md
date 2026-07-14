# RECIPE

How `battery_hash` is computed. This is the whole of it. Nothing is withheld.

## First, the thing that will otherwise waste your time

**The commitment is not the SHA-256 of `battery_v2.json`.**

Hash the file and you get a different number. That is expected. The battery file carries
calibration fields that change legitimately between runs, so a file hash would drift for reasons
that have nothing to do with the questions, and a fingerprint that drifts on its own is useless.

The commitment is the SHA-256 of **the 63 questions**, reduced to a canonical form. The questions
do not change, so the hash does not change.

## The recipe

1. Take the `items` array from the battery.
2. From each item keep exactly **seven** fields, and drop everything else:
   `id`, `family`, `class_label`, `prompt`, `answer`, `answer_type`, `params`.
   `answer` is coerced to a string.
3. Sort the items by `id`.
4. Serialise to JSON with `sort_keys=True`, `ensure_ascii=False`, and separators `(",", ":")`,
   which is to say: keys sorted, unicode kept as unicode, no whitespace anywhere.
5. Encode UTF-8.
6. SHA-256. Hex digest.

Calibration fields are excluded on purpose, and that exclusion is the only judgement call in the
whole procedure. They are per-run measurements, not questions. Including them would mean the
fingerprint of the instrument changed every time we used the instrument.

## The recipe as code

This is the function the measurement runs against, reproduced verbatim:

```python
import hashlib
import json


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
```

`verify.py` in this repository is this function wrapped in a command line. It takes a battery
file, prints the hash it computes, prints the hash stored in the file, and tells you whether they
match. It exits 1 if they do not.

```
$ python3 verify.py battery_v2.json
computed hash: 6c06eb73cdb4a7059c9ade322925b579796cf8a1a1083a02ed961adc3d198034
stored hash:   6c06eb73cdb4a7059c9ade322925b579796cf8a1a1083a02ed961adc3d198034
MATCH
```

Change a single character of a single question and it reports `MISMATCH` and exits 1. That is the
entire security model, and it is enough, because SHA-256 is enough.

## Where this hash is enforced, not merely recorded

The daily measurement recomputes this hash from the questions **before every run** and compares it
to the value stored in the battery. On any mismatch it aborts with
`BATTERY HASH MISMATCH — refusing to log against a changed battery` and writes nothing.

So the battery cannot be edited and quietly kept in service. The instrument stops.

We are aware that you are being asked to take our word for that, because the measurement code is
not public today. The purpose of publishing the recipe and the hash is that at reveal, none of
this rests on our word any more. You will hold the questions, and you will hold a number we
published months earlier, and you can put the two together yourself.
