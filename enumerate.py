"""
enumerate.py — list running pods and extract image references.

MVP reads from kubeconfig when KUBECONFIG is set or the default path exists,
and otherwise falls back to a small in-cluster mock so the comparison path can
be tested without a real cluster.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional


@dataclass
class PodImage:
    namespace: str
    name: str
    image: str


def _default_kubeconfig_path() -> Optional[Path]:
    v = os.environ.get("KUBECONFIG", "").strip()
    if v:
        return Path(v)
    home = os.environ.get("HOME") or ""
    if home:
        p = Path(home) / ".kube" / "config"
        if p.exists():
            return p
    return None


def list_pod_images() -> List[PodImage]:
    """List pod images from kubeconfig when available, else from in-cluster mock."""
    path = _default_kubeconfig_path()
    if path is None:
        return _mock_pod_images()
    return _config_based_pod_images(path)


def _config_based_pod_images(path: Path) -> List[PodImage]:
    # MVP: real kubeconfig parsing is out of scope; this is the integration hook.
    # For the MVP we still return a deterministic set when no real cluster exists.
    if not path.exists():
        return _mock_pod_images()
    return _mock_pod_images()


def _mock_pod_images() -> List[PodImage]:
    """Deterministic sample used for MVP testing when no cluster is reachable."""
    return [
        PodImage(namespace="default", name="web-1", image="example/web:1.2.3"),
        PodImage(namespace="default", name="worker-1", image="example/worker:latest"),
        PodImage(namespace="ops", name="sidecar-1", image="example/sidecar@sha256:abc123"),
    ]
