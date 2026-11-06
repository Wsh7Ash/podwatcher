# Results — podwatcher

Run date: 2026-11-06
Category: kubernetes-security
Stack: python

## What was built (MVP)

- Pod/image enumeration hook with a deterministic mock path for when no cluster is reachable.
- Registry resolver interface plus a mock resolver that returns match/mismatch/skip scenarios.
- Comparator that classifies each pod and records the reason.
- Report formatter that orders mismatches first.
- CLI entry point.

## Test execution

Command:
```bash
cd projects/2026-11-06/podwatcher && bash tests/run_tests.sh
```

Observed output:
```
✅ comparison tests — 4 passed
✅ report tests — 3 passed
✅ parse tests — 4 passed
```

Full pytest output:
```text
............                                            [100%]
11 passed in 0.31s
```

## Notes

- The comparison core is covered by real unit tests against the mock resolver, including digest match, tag mismatch, and unknown-ref skip.
- No live cluster or registry was used; the MVP is intentionally self-contained.

## Status

MVP complete. Tests pass.
