from __future__ import annotations

import json
from pathlib import Path

from .models import RunMetadata


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def write_text(path: Path, content: str) -> None:
    ensure_dir(path.parent)
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, data: dict) -> None:
    ensure_dir(path.parent)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def write_metadata(path: Path, metadata: RunMetadata) -> None:
    write_json(path, metadata.model_dump())
