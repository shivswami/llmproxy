from pathlib import Path

from pdf_md_olmocr.utils import slugify_path


def test_slug_generation():
    assert slugify_path(Path("My File_v2!.pdf")) == "my-file-v2"
    assert slugify_path(Path("***.pdf")) == "document"
