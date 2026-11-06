"""
tests/test_parse.py — image reference parsing tests.
"""
from __future__ import annotations

import pytest

from registry import parse_image_ref


def test_plain_tag():
    assert parse_image_ref("example/app:1.0") == ("example/app", "1.0", None)


def test_digest_only():
    assert parse_image_ref("sha256:abc") == ("", None, "sha256:abc")


def test_digest_with_tag():
    assert parse_image_ref("example/app:1.0@sha256:abc") == ("example/app", "1.0", "sha256:abc")


def test_no_tag_or_digest():
    assert parse_image_ref("example/app") == ("example/app", None, None)
