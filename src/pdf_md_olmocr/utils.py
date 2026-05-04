from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
import re


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def slugify_path(path: Path) -> str:
    stem = path.stem.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", stem).strip("-")
    return slug or "document"
