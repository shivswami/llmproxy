from __future__ import annotations

from pathlib import Path

from .file_ops import write_json
from .models import Manifest, RunMetadata
from .utils import now_iso


def build_manifest(runs: list[RunMetadata]) -> Manifest:
    successes = sum(1 for r in runs if r.status == "success")
    failures = sum(1 for r in runs if r.status == "failed")
    return Manifest(
        generated_at=now_iso(),
        total=len(runs),
        successes=successes,
        failures=failures,
        runs=runs,
    )


def write_manifest(output_root: Path, runs: list[RunMetadata]) -> Path:
    manifest = build_manifest(runs)
    path = output_root / "manifest.json"
    write_json(path, manifest.model_dump())
    return path
