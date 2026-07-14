# nlnl-commitments

Public fingerprints for the instruments **NL;NL Labs** measures with.

**No questions live in this repo, and none will while an instrument is in service.**

## What this is for

NL;NL Labs runs a fixed battery of questions against a pinned model, every day, and publishes what
moves. That is worth nothing unless two things are true:

1. The questions were fixed **before** the measurements began.
2. We cannot quietly change them afterwards to make a result appear.

This repo is where we commit to both, in public, in a form that can be held against us later.

## The commitment

| | |
|---|---|
| Instrument | `battery_v2` |
| Items | 63 |
| SHA-256 | `6c06eb73cdb4a7059c9ade322925b579796cf8a1a1083a02ed961adc3d198034` |
| Questions frozen | 2026-07-11, 02:18:39 UTC |
| First published observation | 2026-07-11, 07:30:24 UTC (5h 11m later) |

Machine-readable: [`battery_v2.commitment.json`](battery_v2.commitment.json)

## ⚠️ This is not `sha256sum battery_v2.json`

If you hash the battery file itself you will get a different number, and that is correct
behaviour, not a discrepancy.

The file carries calibration data that legitimately changes between runs. Hashing the file would
produce a fingerprint that moves for reasons that have nothing to do with the questions. So the
hash is taken over **the 63 questions themselves**, in a fixed canonical form, which is stable.

The exact recipe is in [`RECIPE.md`](RECIPE.md), and [`verify.py`](verify.py) is that recipe as
runnable code. Twenty lines, standard library only, read it in a minute.

## What you can check today, and what you cannot

We would rather say this plainly than let you discover it.

**You cannot, today:**

- Recompute the hash. That needs the 63 questions and the questions are sealed.
- Confirm, without trusting us, that we froze them when we say we did.

**You can, today:**

- Read the recipe and satisfy yourself the hash is precisely defined and reproducible by anyone.
- Run `verify.py` against any battery file of your own and confirm the recipe is real, working
  code rather than a description of code.
- Hold us to a number that is now published and dated. Every observation we publish from here is
  a bet against this string.

**You can, at reveal:**

- Run `python3 verify.py battery_v2.json` against the file we release. If it does not print
  `6c06eb73…034`, we changed the questions and lied about it, and you will be able to prove it in
  one command. See [`REVEAL.md`](REVEAL.md).

## The timestamp: how to check the date without trusting us

`battery_v2.commitment.json.ots` is an [OpenTimestamps](https://opentimestamps.org) proof. It
anchors this commitment into the Bitcoin blockchain.

```
$ ots verify battery_v2.commitment.json.ots
```

That tells you this exact file, containing this exact hash, **existed on or before a specific
Bitcoin block**. We cannot rewrite Bitcoin. So even though we control this repository and could
force-push it, **we cannot move the date.**

What it proves is narrow and we will not dress it up: **the commitment existed by then.** It says
nothing about whether the questions are any good, and nothing about whether we ran them.

**Status: submitted 14 July 2026, awaiting Bitcoin confirmation.** Until a block confirms it,
`ots verify` reports `Pending confirmation in Bitcoin blockchain` and the proof rests on the
calendar servers rather than on Bitcoin itself. We will commit the completed proof the moment it
lands. **If you are reading this long after 14 July and it still says pending, we did not follow
through, and you should hold that against us.**

## The four things this does not prove

**1. The anchor is dated later than the first observations.** We stamped it on **14 July 2026**.
The first four days of published data (**11 to 14 July**) therefore **predate the anchor**. For
those four days the commitment rests on our own git history and our own run logs, which we will
open at reveal. **From the anchor forward it is airtight. For those four days, it is our word.**
Nobody else in this space would tell you that. That is why we are telling you.

**2. The freeze timestamp is our own record.** Our logs say `battery_v2` was created at 02:18:39
UTC on 11 July and that the first measured item ran at 07:30:24 UTC the same morning, five hours
and eleven minutes later. Every logged row of every run since carries this hash and no other. The
run recomputes the hash from the questions before it starts and **aborts if it does not match**,
so we cannot edit the battery and quietly keep measuring. But that is our code and our logs.

**3. There was a `battery_v1`.** It had 52 items and was created 45 minutes earlier the same
morning. It produced **zero logged rows** and appears in **no published number**. It was
superseded before the first measurement existed. We are telling you this unprompted because it is
named in the commitment file, and a rating agency whose first record is preceded by a discarded
instrument should say so out loud rather than wait to be asked.

**4. ★ We do not prove the measurements happened at all.** Nothing here proves what we sent to the
API or what came back. OpenAI does not sign its responses, so there is no cryptographic path from
their servers to this page. In principle we could be inventing every number.

We are telling you where our proof stops because a rating agency that hides its own limits is just
one more organisation asking to be trusted.

## Why the questions stay sealed

Publish the questions and any provider can tune against them. The scores would keep moving and
would stop meaning anything, and we would never know the exact day it happened.

A sealed battery with a public fingerprint is the only version of this that survives contact with
the thing it measures.

## Licence

The fingerprints and documents in this repository are public. Reuse them, check them, cite them.
