from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from .file_ops import ensure_dir, write_metadata, write_text
from .models import AppConfig, RunMetadata
from .olmocr_adapter import run_olmocr
from .utils import slugify_path


def _resolve_run_paths(config: AppConfig, pdf_path: Path, force: bool = False) -> tuple[str, Path, Path]:
    base_slug = slugify_path(pdf_path)
    slug = base_slug
    out_dir = config.output_root / slug
    if out_dir.exists() and not force:
        slug = f"{base_slug}-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}"
        out_dir = config.output_root / slug
    workspace = config.workspace_root / slug
    return slug, out_dir, workspace


def convert_pdf(config: AppConfig, pdf_path: Path, force: bool = False) -> RunMetadata:
    started = datetime.now(timezone.utc)
    slug, out_dir, workspace_dir = _resolve_run_paths(config, pdf_path, force=force)
    ensure_dir(out_dir)
    ensure_dir(workspace_dir)
    md_path = out_dir / f"{slug}.md"
    run_log = out_dir / "run.log"

    try:
        result = run_olmocr(config, workspace_dir, pdf_path)
        write_text(run_log, (result.stdout or "") + "\n" + (result.stderr or ""))
        if result.returncode != 0:
            raise RuntimeError(f"olmocr failed with code {result.returncode}")

        generated_md = workspace_dir / f"{pdf_path.stem}.md"
        if generated_md.exists():
            write_text(md_path, generated_md.read_text(encoding="utf-8"))
        else:
            write_text(md_path, result.stdout or "")

        status = "success"
        error = None
    except Exception as exc:
        status = "failed"
        error = str(exc)

    ended = datetime.now(timezone.utc)
    metadata = RunMetadata(
        pdf_path=str(pdf_path),
        slug=slug,
        status=status,
        started_at=started.isoformat(),
        ended_at=ended.isoformat(),
        duration_seconds=(ended - started).total_seconds(),
        md_path=str(md_path) if status == "success" else None,
        run_log_path=str(run_log),
        error=error,
    )
    write_metadata(out_dir / "metadata.json", metadata)
    return metadata
