"""
registry.py — registry image resolver interface and a basic implementation.

MVP defines a resolver interface and a simple no-op/mock resolver so the
comparison path can be tested without contacting real registries.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class RegistryAnswer:
    """What the registry says about an image reference."""

    ref: str
    digest: Optional[str] = None
    tag: Optional[str] = None
    error: Optional[str] = None

    @property
    def matched(self) -> bool:
        return self.error is None


class RegistryResolver(ABC):
    """Abstract registry resolver."""

    @abstractmethod
    def resolve(self, image: str) -> RegistryAnswer:
        raise NotImplementedError


class MockRegistryResolver(RegistryResolver):
    """Mock resolver for MVP testing.

    - ``example/web:1.2.3`` returns the same digest the pod is running, so the
      comparison reports a digest match.
    - ``example/worker:latest`` returns a different digest than the running value,
      so the comparison reports drift on a ``:latest`` image without changing the tag.
    - ``example/sidecar@sha256:abc123`` returns the same digest as the running ref,
      so the comparison reports a digest match.
    - unknown refs return an error.
    """

    def resolve(self, image: str) -> RegistryAnswer:
        if image == "example/web:1.2.3":
            return RegistryAnswer(ref=image, digest="sha256:web123", tag="1.2.3", error=None)
        if image == "example/worker:latest":
            # worker:latest is claimed by the registry at a different digest than the pod
            # runs, so the comparison can observe drift on the ``:latest`` image.
            return RegistryAnswer(ref=image, digest="worker-drifted", tag="latest", error=None)
        if image == "example/sidecar@sha256:abc123":
            return RegistryAnswer(ref=image, digest="sha256:abc123", tag=None, error=None)
        return RegistryAnswer(ref=image, error="unknown ref in mock registry")


def parse_image_ref(image: str) -> tuple[str, Optional[str], Optional[str]]:
    """Return (name, tag_or_none, digest_or_none)."""
    if image.startswith("sha256:"):
        return ("", None, image)
    if "@" in image:
        name_part, digest = image.split("@", 1)
        tag: Optional[str] = None
        if ":" in name_part:
            name, tag = name_part.rsplit(":", 1)
        else:
            name = name_part
        return (name, tag, digest)
    if ":" in image:
        name, tag = image.rsplit(":", 1)
        return (name, tag, None)
    return (image, None, None)
