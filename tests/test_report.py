"""
tests/test_report.py — report formatting tests.
"""
from __future__ import annotations

import pytest

from compare import Classification, PodComparison
from report import format_report


def _comparison(cls, image="example/app:1.0"):
    return PodComparison(namespace="ns", name="pod-1", image=image, classification=cls, reason="ok")


def test_report_includes_mismatch():
    report = format_report([_comparison(Classification.MISMATCH)])
    assert "MISMATCH" in report
    assert "example/app:1.0" in report


def test_report_empty_when_no_comparisons():
    assert format_report([]) == "No pods compared.\n"


def test_report_order_mismatch_first():
    report = format_report([
        _comparison(Classification.MATCH),
        _comparison(Classification.MISMATCH),
    ])
    lines = report.splitlines()
    asserts = [i for i, line in enumerate(lines) if line.startswith("MISMATCH")]
    assert asserts
    mismatch_idx = asserts[0]
    match_idx = next(i for i, line in enumerate(lines) if line.startswith("MATCH"))
    assert mismatch_idx < match_idx
