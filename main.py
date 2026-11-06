"""
main.py — CLI entry point for podwatcher.
"""

from __future__ import annotations

import argparse
import sys

from enumerate import list_pod_images
from registry import MockRegistryResolver
from compare import compare_pods
from report import format_report


def main(argv=None):
    ap = argparse.ArgumentParser(prog="podwatcher", description="Audit running pod image drift")
    ap.add_argument("--registry", choices=["mock"], default="mock", help="Registry resolver to use")
    args = ap.parse_args(argv)

    pods = list_pod_images()
    if not pods:
        print("No pods found.")
        return 0

    resolver: "RegistryResolver"
    if args.registry == "mock":
        resolver = MockRegistryResolver()
    else:
        print("Unsupported registry resolver.", file=sys.stderr)
        return 2

    comparisons = compare_pods(pods, resolver)
    print(format_report(comparisons))
    mismatches = [c for c in comparisons if c.classification.name == "MISMATCH"]
    return 1 if mismatches else 0


if __name__ == "__main__":
    raise SystemExit(main())
