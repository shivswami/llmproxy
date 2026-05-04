from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field


class AppConfig(BaseModel):
    base_url: str = "http://localhost:1234/v1"
    model_name: str = "olmocr2"
    workspace_root: Path = Path("./runs")
    output_root: Path = Path("./output")
    timeout_seconds: int = 7200
    olmocr_path: str = "olmocr"


class PreflightResult(BaseModel):
    lm_studio_ok: bool
    olmocr_ok: bool
    output_writable: bool
    details: list[str] = Field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.lm_studio_ok and self.olmocr_ok and self.output_writable


class RunMetadata(BaseModel):
    pdf_path: str
    slug: str
    status: str
    started_at: str
    ended_at: str
    duration_seconds: float
    md_path: Optional[str] = None
    run_log_path: Optional[str] = None
    error: Optional[str] = None


class Manifest(BaseModel):
    generated_at: str
    total: int
    successes: int
    failures: int
    runs: list[RunMetadata] = Field(default_factory=list)


@dataclass
class CliOverrides:
    base_url: Optional[str] = None
    model_name: Optional[str] = None
    workspace_root: Optional[Path] = None
    output_root: Optional[Path] = None
    timeout_seconds: Optional[int] = None
    olmocr_path: Optional[str] = None
