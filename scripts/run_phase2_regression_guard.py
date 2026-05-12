"""Run the HL-ImageNet Phase 2 regression guard layer.

Local-safe runner:
- Adds repository root to sys.path before importing hlinet.
- Emits JSON/Markdown regression-guard artifacts.
- Does not change classifier behavior.
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from hlinet.eval.regression_guard import main


if __name__ == "__main__":
    main()