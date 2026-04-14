from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOOLS_DIR = ROOT / "tools"
API_DIR = ROOT / "apps" / "master-persona-builder" / "api"

for p in (TOOLS_DIR, API_DIR):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

