# Starts the API locally on Windows PowerShell. Run from the repository root.
$ErrorActionPreference = "Stop"
Set-Location "services\api"
if (-not (Test-Path ".venv")) {
    python -m venv .venv
}
.\.venv\Scripts\Activate.ps1
pip install -r ..\..\services\api\requirements.txt --quiet
uvicorn main:app --reload --host 127.0.0.1 --port 8000
