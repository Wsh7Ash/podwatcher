# podwatcher

A small auditor that reports when running pods are using images that no longer match what the registry says. It focuses on the comparison and the report: match, mismatch, and skip reasons.

## What it does

- Lists running pods and extracts image references.
- Resolves each image reference through a registry resolver.
- Classifies each pod as `match`, `mismatch`, or `skip`.
- Prints a drift report ordered with mismatches first.

## Run locally

```bash
cd podwatcher
python main.py
```

The MVP uses a mock registry resolver so it can run and demonstrate the comparison path without contacting a real registry. A real registry resolver is the natural next step once cluster and registry access are available.

## Output

The report lists mismatches, then skips, then matches, each with the pod, image, and reason.

## Limitations

- The MVP does not connect to a real Kubernetes cluster or a real registry; it uses a local mock for both enumeration and resolution.
- Digest/tag semantics are simplified for the comparison core.

## Security notes

See `SECURITY.md` for notes about cluster and registry access.

## Project structure

- `enumerate.py` — pod/image enumeration hook.
- `registry.py` — resolver interface and mock.
- `compare.py` — classification logic.
- `report.py` — report formatting.
- `main.py` — CLI.
- `tests/` — pytest suite.
- `SECURITY.md` — security notes.
- `LICENSE` — MIT.
