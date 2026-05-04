# pdf-md-olmocr

`pdf-md-olmocr` is a local-first CLI that converts PDFs to Markdown using:
- `olmocr` in remote inference mode
- LM Studio OpenAI-compatible local server (`http://localhost:1234/v1`)

## Features
- `pdfmd check` preflight validation
- `pdfmd convert <pdf_path>` single conversion
- `pdfmd batch <folder_path>` batch conversion with continue-on-failure
- `pdfmd manifest` regenerate `output/manifest.json`

## Setup (macOS primary, also works on Linux/Windows)

### 1) Clone the repository
```bash
git clone <your-repo-url>
cd pdf-md-olmocr
```

### 2) Create a virtual environment with uv
```bash
uv venv
# macOS/Linux
source .venv/bin/activate
# Windows (PowerShell)
# .venv\Scripts\Activate.ps1
```

### 3) Install dependencies with uv
```bash
uv sync
```

### 4) Install olmocr
```bash
pip install olmocr
```

### 5) Start LM Studio server
In LM Studio:
1. Load a model (example: `allenai/olmocr-2-7b`)
2. Start local server at `http://localhost:1234/v1`

### 6) Run preflight
```bash
uv run pdfmd check
```

## Configuration
Defaults are read from `config/default.yaml`:
- `base_url=http://localhost:1234/v1`
- `model_name=olmocr2`
- `workspace_root=./runs`
- `output_root=./output`
- `timeout_seconds=7200`

Environment variable overrides:
- `PDFMD_BASE_URL`
- `PDFMD_MODEL_NAME`
- `PDFMD_WORKSPACE_ROOT`
- `PDFMD_OUTPUT_ROOT`
- `PDFMD_TIMEOUT_SECONDS`
- `PDFMD_OLMOCR_PATH`

CLI overrides are available on `convert`.

## Usage
```bash
uv run pdfmd check
uv run pdfmd convert ./docs/file.pdf
uv run pdfmd batch ./docs
uv run pdfmd manifest
```

## Output layout
For each PDF:
- `output/<slug>/<slug>.md`
- `output/<slug>/metadata.json`
- `output/<slug>/run.log`

Global summary:
- `output/manifest.json`
