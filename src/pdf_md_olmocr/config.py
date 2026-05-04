from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

from .models import AppConfig, CliOverrides


def _load_yaml(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}
        return data if isinstance(data, dict) else {}


def _load_env() -> dict[str, Any]:
    mapping = {
        "base_url": os.getenv("PDFMD_BASE_URL"),
        "model_name": os.getenv("PDFMD_MODEL_NAME"),
        "workspace_root": os.getenv("PDFMD_WORKSPACE_ROOT"),
        "output_root": os.getenv("PDFMD_OUTPUT_ROOT"),
        "timeout_seconds": os.getenv("PDFMD_TIMEOUT_SECONDS"),
        "olmocr_path": os.getenv("PDFMD_OLMOCR_PATH"),
    }
    return {k: v for k, v in mapping.items() if v not in (None, "")}


def load_config(overrides: CliOverrides | None = None) -> AppConfig:
    root = Path.cwd()
    yaml_data = _load_yaml(root / "config" / "default.yaml")
    env_data = _load_env()
    cli_data = {
        k: v
        for k, v in (overrides.__dict__.items() if overrides else [])
        if v is not None
    }
    merged = {**yaml_data, **env_data, **cli_data}
    return AppConfig(**merged)
