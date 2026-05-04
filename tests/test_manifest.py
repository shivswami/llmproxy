import json

from pdf_md_olmocr.manifest import write_manifest
from pdf_md_olmocr.models import RunMetadata


def test_manifest_writing(tmp_path):
    runs = [
        RunMetadata(
            pdf_path="a.pdf",
            slug="a",
            status="success",
            started_at="2024-01-01T00:00:00+00:00",
            ended_at="2024-01-01T00:00:01+00:00",
            duration_seconds=1.0,
            md_path="output/a/a.md",
        )
    ]
    path = write_manifest(tmp_path, runs)
    data = json.loads(path.read_text(encoding="utf-8"))
    assert data["total"] == 1
    assert data["successes"] == 1
