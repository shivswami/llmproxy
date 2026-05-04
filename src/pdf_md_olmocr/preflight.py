from __future__ import annotations

import shutil
from pathlib import Path

import httpx

from .models import AppConfig, PreflightResult


def _is_output_writable(path: Path) -> bool:
    try:
        path.mkdir(parents=True, exist_ok=True)
        test_file = path / ".write_test"
        test_file.write_text("ok", encoding="utf-8")
        test_file.unlink(missing_ok=True)
        return True
    except OSError:
        return False


def run_preflight(config: AppConfig) -> PreflightResult:
    details: list[str] = []

    try:
        resp = httpx.get(f"{config.base_url.rstrip('/')}/models", timeout=10)
        lm_ok = resp.status_code < 500
        details.append(f"LM Studio reachable: status={resp.status_code}")
    except Exception as exc:
        lm_ok = False
        details.append(f"LM Studio not reachable: {exc}")

    olmocr_found = shutil.which(config.olmocr_path) is not None
    details.append(f"olmocr executable {'found' if olmocr_found else 'not found'}: {config.olmocr_path}")

    writable = _is_output_writable(config.output_root)
    details.append(f"Output writable: {writable} ({config.output_root})")

    return PreflightResult(
        lm_studio_ok=lm_ok,
        olmocr_ok=olmocr_found,
        output_writable=writable,
        details=details,
    )
