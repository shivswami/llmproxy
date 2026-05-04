from __future__ import annotations

from pathlib import Path

import typer

from .config import load_config
from .logging_utils import setup_logging
from .manifest import write_manifest
from .models import CliOverrides
from .preflight import run_preflight
from .runner import convert_pdf

app = typer.Typer(help="PDF to Markdown using olmOCR + LM Studio")


def _overrides(base_url: str | None, model_name: str | None, workspace_root: Path | None, output_root: Path | None, timeout_seconds: int | None, olmocr_path: str | None) -> CliOverrides:
    return CliOverrides(
        base_url=base_url,
        model_name=model_name,
        workspace_root=workspace_root,
        output_root=output_root,
        timeout_seconds=timeout_seconds,
        olmocr_path=olmocr_path,
    )


@app.command("check")
def check(verbose: bool = False):
    setup_logging(verbose)
    cfg = load_config()
    result = run_preflight(cfg)
    for line in result.details:
        typer.echo(line)
    raise typer.Exit(code=0 if result.ok else 1)


@app.command("convert")
def convert(
    pdf_path: Path,
    force: bool = False,
    base_url: str | None = None,
    model_name: str | None = None,
    workspace_root: Path | None = None,
    output_root: Path | None = None,
    timeout_seconds: int | None = None,
    olmocr_path: str | None = None,
):
    cfg = load_config(_overrides(base_url, model_name, workspace_root, output_root, timeout_seconds, olmocr_path))
    run = convert_pdf(cfg, pdf_path, force=force)
    manifest_path = write_manifest(cfg.output_root, [run])
    typer.echo(f"{run.status}: {run.pdf_path} -> {run.md_path}")
    typer.echo(f"manifest: {manifest_path}")
    raise typer.Exit(code=0 if run.status == "success" else 1)


@app.command("batch")
def batch(folder_path: Path, force: bool = False):
    cfg = load_config()
    runs = []
    for pdf in sorted(folder_path.glob("*.pdf")):
        run = convert_pdf(cfg, pdf, force=force)
        runs.append(run)
        typer.echo(f"{run.status}: {pdf}")
    manifest_path = write_manifest(cfg.output_root, runs)
    failures = [r for r in runs if r.status == "failed"]
    typer.echo(f"manifest: {manifest_path}")
    raise typer.Exit(code=1 if failures else 0)


@app.command("manifest")
def manifest_cmd(output_root: Path = Path("./output")):
    cfg = load_config(CliOverrides(output_root=output_root))
    runs = []
    for metadata in cfg.output_root.glob("*/metadata.json"):
        import json

        payload = json.loads(metadata.read_text(encoding="utf-8"))
        from .models import RunMetadata

        runs.append(RunMetadata(**payload))
    path = write_manifest(cfg.output_root, runs)
    typer.echo(f"wrote {path}")


if __name__ == "__main__":
    app()
