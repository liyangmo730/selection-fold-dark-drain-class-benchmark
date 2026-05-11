# Reproducibility Notes

This release is intentionally curated. It contains only the manuscript-facing inputs needed to reproduce the figures, tables, dense z=0 matter-power window check, and compressed S8 comparison. It excludes old exploratory outputs, failed scans, debug logs, prompts, and internal claim-boundary drafts.

## Quick Reproduction

1. Install Python dependencies:

   ```bash
   python -m pip install -r environment/requirements.txt
   ```

2. Regenerate figures, the compressed S8 table, and the windowed sigma8 table:

   ```bash
   python scripts/build_all_figures.py
   ```

3. Build the paper, if LaTeX is installed:

   ```bash
   cd paper
   latexmk -pdf paper.tex
   ```

## What Is Reproduced

- Mechanism schematic.
- Background handoff diagnostic figure.
- Source-layer redshift relaxation figure.
- Dynamic-response comparison figure.
- Newtonian-gauge benchmark/proxy branch figure.
- S8-facing proxy amplitude ladder.
- Compressed S8 amplitude comparison figure and table.
- Windowed sigma8 amplitude check from dense z=0 matter-power arrays.

## Scope Boundary

The repository does not include a full CLASS source tree, a DES/KiDS/HSC/Planck likelihood pipeline, nonlinear modeling, nuisance marginalization, covariance matrices, or a gauge-complete Boltzmann closure.
