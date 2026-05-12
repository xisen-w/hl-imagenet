"""Run the HL-ImageNet Phase 2 diagnostic lens.

Local-safe runner:
- Adds repository root to sys.path before importing hlinet.
- Does not change classifier behavior.
- Only runs diagnostics over existing Phase 2 logs.
"""

from __future__ import annotations

import sys
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]

if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from hlinet.eval.diagnostics import main


if __name__ == "__main__":
    main()
