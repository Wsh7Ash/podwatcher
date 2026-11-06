"""
report.py — formatting for drift reports.
"""

from __future__ import annotations

from typing import List

from compare import Classification, PodComparison


def format_report(comparisons: List[PodComparison]) -> str:
    if not comparisons:
        return "No pods compared.\n"

    lines: List[str] = []
    lines.append("Pod image drift report")
    lines.append("=====================")
    lines.append("")

    by_cls: dict[Classification, List[PodComparison]] = {
        Classification.MATCH: [],
        Classification.MISMATCH: [],
        Classification.SKIP: [],
    }
    for c in comparisons:
        by_cls.setdefault(c.classification, []).append(c)

    for cls in (Classification.MISMATCH, Classification.SKIP, Classification.MATCH):
        items = by_cls.get(cls, [])
        if not items:
            continue
        lines.append(f"{cls.value.upper()} ({len(items)}):")
        for c in items:
            lines.append(f"  - {c.namespace}/{c.name}: {c.image}")
            lines.append(f"    reason: {c.reason}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"
