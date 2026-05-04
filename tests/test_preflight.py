from pdf_md_olmocr.models import AppConfig
from pdf_md_olmocr.preflight import run_preflight


class DummyResp:
    def __init__(self, code: int):
        self.status_code = code


def test_preflight_checks(tmp_path, monkeypatch):
    cfg = AppConfig(output_root=tmp_path)

    monkeypatch.setattr("pdf_md_olmocr.preflight.httpx.get", lambda *args, **kwargs: DummyResp(200))
    monkeypatch.setattr("pdf_md_olmocr.preflight.shutil.which", lambda _: "/usr/bin/olmocr")

    result = run_preflight(cfg)
    assert result.lm_studio_ok is True
    assert result.olmocr_ok is True
    assert result.output_writable is True
