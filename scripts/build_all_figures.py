#!/usr/bin/env python3
"""Run all figure/table regeneration steps for the release."""
import subprocess
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
for script in [
    "make_submission_figures.py",
    "build_s8_compressed_comparison.py",
    "build_sigma8_window_check.py",
]:
    subprocess.check_call([sys.executable, str(ROOT / "scripts" / script)])
