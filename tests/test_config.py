from pathlib import Path

from pdf_md_olmocr.config import load_config
from pdf_md_olmocr.models import CliOverrides


def test_config_loading_defaults(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "default.yaml").write_text(
        "base_url: http://localhost:1234/v1\nmodel_name: olmocr2\nworkspace_root: ./runs\noutput_root: ./output\ntimeout_seconds: 7200\n",
        encoding="utf-8",
    )
    cfg = load_config()
    assert cfg.base_url == "http://localhost:1234/v1"
    assert cfg.timeout_seconds == 7200


def test_config_env_and_cli_override(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    (tmp_path / "config").mkdir()
    (tmp_path / "config" / "default.yaml").write_text("model_name: base\n", encoding="utf-8")
    monkeypatch.setenv("PDFMD_MODEL_NAME", "from_env")
    cfg = load_config(CliOverrides(model_name="from_cli", output_root=Path("./x")))
    assert cfg.model_name == "from_cli"
    assert str(cfg.output_root) == "x"
