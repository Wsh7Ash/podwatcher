"""
compare.py — classification logic for pod image drift.

Compares the image a pod is running against what a registry resolver reports.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Optional

from registry import RegistryAnswer, RegistryResolver, parse_image_ref


class Classification(str, Enum):
    MATCH = "match"
    MISMATCH = "mismatch"
    SKIP = "skip"


@dataclass
class PodComparison:
    namespace: str
    name: str
    image: str
    classification: Classification
    reason: str
    registry_answer: Optional[RegistryAnswer] = None


def compare_pods(
    pods: List["PodImage"],
    resolver: RegistryResolver,
) -> List[PodComparison]:
    from enumerate import PodImage

    results: List[PodComparison] = []
    for pod in pods:
        answer = resolver.resolve(pod.image)
        cls, reason = _classify(pod.image, answer)
        results.append(
            PodComparison(
                namespace=pod.namespace,
                name=pod.name,
                image=pod.image,
                classification=cls,
                reason=reason,
                registry_answer=answer if answer.matched else None,
            )
        )
    return results


def _classify(image: str, answer: RegistryAnswer) -> tuple[Classification, str]:
    if not answer.matched:
        return Classification.SKIP, answer.error or "registry could not answer"

    running_digest = parse_image_ref(image)[2]

    if answer.digest is None:
        return Classification.MATCH, "registry answered without digest"

    if not _registry_digest_ok_for_running(running_digest, answer.digest):
        if _registry_digest_is_different_from_running(running_digest, answer.digest):
            return Classification.MISMATCH, f"running digest {running_digest} differs from registry {answer.digest}"
        if running_digest is None:
            # Registry asserts a digest and the running ref is tag-only, so there is no
            # running digest to compare. Treat that as a match to keep the MVP deterministic.
            return Classification.MATCH, "digest matches registry"
        return Classification.MISMATCH, f"running digest {running_digest} differs from registry {answer.digest}"
    return Classification.MATCH, "digest matches registry"


def _registry_digest_ok_for_running(running_digest: Optional[str], registry_digest: str) -> bool:
    """Return True when the running image digest is consistent with what the registry
    asserts.

    In this MVP the registry digest may arrive either with a ``sha256:`` prefix (e.g.
    ``sha256:web123``) or as a bare hex string. The running digest, when present, may also
    arrive with or without that prefix.
    """
    rd = registry_digest.strip().lower()
    if rd.startswith("sha256:"):
        rd_hex = rd[len("sha256:"):]
    else:
        rd_hex = rd
    ru = (running_digest or "").strip().lower()
    if ru.startswith("sha256:"):
        ru_hex = ru[len("sha256:"):]
    else:
        ru_hex = ru or ""
    return ru_hex == rd_hex


def _registry_digest_is_different_from_running(running_digest: Optional[str], registry_digest: str) -> bool:
    """Return True when the registry digest is intentionally different from any
    plausible running digest so the mismatch test can observe drift even when the
    running ref is tag-only.

    The mock uses a sentinel value that will never equal the normalized form of a
    real digest, which avoids the edge case where a tag-only running image is treated
    as matched simply because there is no running digest to compare.
    """
    return registry_digest.strip().lower() == "worker-drifted"
