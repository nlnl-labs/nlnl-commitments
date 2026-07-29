# RECIPE

How `battery_hash` is computed. This is the whole of it. Nothing is withheld.

There are eight sealed instruments in this repository and **two** recipes. Seven use the
canonical items recipe described below. One, the gateway probe set, is hashed a different
way, and that exception is spelled out at the end rather than buried.

| commitment file | what it seals | recipe |
| --- | --- | --- |
| `battery_v2.commitment.json` | the 63-question daily exam | canonical items |
| `swap.commitment.json` | 100 forced-choice items | canonical items |
| `time_of_day.commitment.json` | 10 items, **a subset of the exam** | canonical items |
| `repeat.commitment.json` | 4 items, asked ten times a day | canonical items |
| `refusal.commitment.json` | 40 items | canonical items |
| `long_memory.commitment.json` | 4 long-document items | canonical items |
| `tokenizer.commitment.json` | 12 round-trip strings | canonical items |
| `or_gateway_probes_v1.commitment.json` | 36 gateway probes | **whole file bytes** |

Two things about that table we would rather you heard from us than worked out yourself.

**`time_of_day` is not an eighth independent instrument.** Its ten items are ten of the
sixty-three exam questions, taken unchanged. It is the exam asked at a different hour. Its
commitment file says so, and its reveal cannot happen separately from the exam's.

**Only `battery_v2` was committed before it started measuring.** The other seven were sealed
in code, enforced from the day they were sealed, and publicly committed on 29 July 2026 —
between six and fourteen days later. Each commitment file names its own gap. For those days
the seal rests on our own code and our own git history rather than on a public timestamp.

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
recipe:        canonical items (expected hash read from the file's battery_hash)
computed hash: 6c06eb73cdb4a7059c9ade322925b579796cf8a1a1083a02ed961adc3d198034
stored hash:   6c06eb73cdb4a7059c9ade322925b579796cf8a1a1083a02ed961adc3d198034
MATCH
```

Change a single character of a single question and it reports `MISMATCH` and exits 1. That is the
entire security model, and it is enough, because SHA-256 is enough.

It prints the recipe it used on the first line, so you are never guessing which of the two you
just checked. Hand it a file it does not recognise and it refuses rather than guessing.

## The exception: the gateway probe set

`or_gateway_probes_v1.json` is hashed as **the raw bytes of the whole file**:

```python
import hashlib

hashlib.sha256(open("or_gateway_probes_v1.json", "rb").read()).hexdigest()
```

That is the plain thing the recipe above deliberately is not, and the reason is that the
objection which forced the canonical recipe does not apply here. The exam battery carries
per-run calibration fields, so hashing the file would make the fingerprint drift every time the
instrument was used. The probe set carries nothing of the kind. There is nothing to strip, so
there is nothing to canonicalise, and the bytes are the instrument.

One consequence you should know about, because it changes how you check it. A file hashed by its
own bytes cannot carry its own hash — writing the number into the file changes the bytes and
therefore changes the number. So the expected hash is not in the probe file. It is in
`or_gateway_probes_v1.commitment.json`, and `verify.py` takes it as a second argument:

```
$ python3 verify.py or_gateway_probes_v1.json 34fb446cf8afc8cdf9ba104b8a90ba6f3e19158251d722b5c69e00c5fecb565f
recipe:        whole file bytes (expected hash given on the command line)
computed hash: 34fb446cf8afc8cdf9ba104b8a90ba6f3e19158251d722b5c69e00c5fecb565f
stored hash:   34fb446cf8afc8cdf9ba104b8a90ba6f3e19158251d722b5c69e00c5fecb565f
MATCH
```

You have to supply that number yourself. That is on purpose. A verifier that ships with the
answer inside it is checking itself, and proves nothing. Take the hash from the commitment file,
from the site, or from the timestamp proof, and hand it to the checker separately.

## Where this hash is enforced, not merely recorded

The daily measurement recomputes this hash from the questions **before every run** and compares it
to the value stored in the battery. On any mismatch it aborts with
`BATTERY HASH MISMATCH — refusing to log against a changed battery` and writes nothing.

So the battery cannot be edited and quietly kept in service. The instrument stops.

We are aware that you are being asked to take our word for that, because the measurement code is
not public today. The purpose of publishing the recipe and the hash is that at reveal, none of
this rests on our word any more. You will hold the questions, and you will hold a number we
published months earlier, and you can put the two together yourself.
