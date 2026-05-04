from __future__ import annotations

import subprocess
from pathlib import Path

from .models import AppConfig


def run_olmocr(config: AppConfig, workspace_dir: Path, pdf_path: Path, timeout: int | None = None) -> subprocess.CompletedProcess[str]:
    cmd = [
        config.olmocr_path,
        str(workspace_dir),
        "--server",
        config.base_url,
        "--model",
        config.model_name,
        "--markdown",
        "--pdfs",
        str(pdf_path),
    ]
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout or config.timeout_seconds)
