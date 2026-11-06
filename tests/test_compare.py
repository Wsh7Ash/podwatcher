"""
tests/test_compare.py — comparison classification tests.
"""
from __future__ import annotations

import pytest

from compare import Classification, compare_pods
from registry import MockRegistryResolver


def _pod(image):
    return type("Pod", (), {"namespace": "ns", "name": "p", "image": image})()


def test_match_on_digest():
    resolver = MockRegistryResolver()
    results = compare_pods([_pod("example/web:1.2.3")], resolver)
    assert len(results) == 1
    assert results[0].classification == Classification.MATCH
    assert results[0].reason.startswith("digest matches")


def test_mismatch_on_digest():
    resolver = MockRegistryResolver()
    results = compare_pods([_pod("example/worker:latest")], resolver)
    assert results[0].classification == Classification.MISMATCH
    assert "differs" in results[0].reason


def test_skip_on_unknown_ref():
    resolver = MockRegistryResolver()
    results = compare_pods([_pod("unknown/image:latest")], resolver)
    assert results[0].classification == Classification.SKIP
    assert "unknown" in results[0].reason


def test_digest_drift_classification():
    resolver = MockRegistryResolver()
    results = compare_pods([_pod("example/sidecar@sha256:abc123")], resolver)
    assert results[0].classification == Classification.MATCH
    assert results[0].reason.startswith("digest matches")
