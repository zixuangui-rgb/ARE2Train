#!/usr/bin/env python3
"""Run ARE2Train environment checks from a source checkout."""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from are2train.doctor import main  # noqa: E402


if __name__ == "__main__":
    raise SystemExit(main())
