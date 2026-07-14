# REVEAL

A fingerprint nobody can ever check is decoration. This is the promise that turns it into a
commitment, and the promise is falsifiable.

## The promise

**When `battery_v2` is retired and replaced, we publish `battery_v2.json` in full, in this
repository, including all 63 questions and their answers.**

Not a summary. Not a sample. The file.

## What you do with it

```
$ python3 verify.py battery_v2.json
```

If it prints `6c06eb73cdb4a7059c9ade322925b579796cf8a1a1083a02ed961adc3d198034` and `MATCH`, then
the questions you are holding are the questions we committed to on 11 July 2026, and every
observation we published against `battery_v2` was measured on them.

If it prints anything else, we changed the instrument and did not say so. You will be able to
prove that in one command, and you should say so loudly.

That is the deal. It is deliberately one-sided.

## Why the trigger is a condition and not a date

A retirement is a thing we control and can state honestly. A date is a thing we would have to walk
back the first time reality got in the way, and a walked-back promise is worse than no promise.

The condition is not open-ended in practice. A battery is retired when it stops discriminating,
which is to say when it can no longer tell a changed model from an unchanged one, and that is a
measurable event rather than a matter of taste.

## Why not now

Publish the questions today and any provider can tune against them. Scores would keep moving and
would stop meaning anything, and the failure would be silent. We would be running an instrument
that reports numbers and measures nothing, which is precisely the condition NL;NL Labs exists to
detect in other people's systems.

The sealed battery is not secrecy for its own sake. It is the only configuration in which the
measurement survives being published.

## What we have not promised

We have not promised a reveal date. We have not promised that `battery_v2` will be retired within
any particular window. We have promised what happens when it is, and we have published the number
that makes the promise checkable.

If we retire `battery_v2` and this file does not appear, that is your answer about us.
