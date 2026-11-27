"""Puts services/api on sys.path so tests import the same packages the running API uses."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for p in (ROOT / "services" / "api", ROOT / "services"):
    sys.path.insert(0, str(p))
