# CLASS Benchmark for Fold-Triggered Dark-Matter Mass Drain

This repository is a curated reproducibility release for the manuscript "A CLASS Benchmark for Late-Time Matter-Power Suppression from a Fold-Triggered Dark-Matter Mass Drain."

Repository URL: https://github.com/liyangmo730/selection-fold-dark-drain-class-benchmark

## Scope

This release reproduces the benchmark tables, figures, dense z=0 matter-power arrays, windowed sigma8 amplitude check, and compressed S8 comparison used in the paper.

It is not a DES/KiDS/HSC/Planck likelihood pipeline and does not provide a gauge-complete Boltzmann closure. It is not a full public CLASS implementation; it reproduces the manuscript tables and figures from archived benchmark outputs.

## Repository Layout

- `paper/`: manuscript source, bibliography, local table inputs, and generated figures.
- `data/`: curated numerical inputs for background, matter-power, dense z=0 spectra, response, sigma8, and compressed S8 summaries.
- `scripts/`: scripts that regenerate the manuscript figures, compressed S8 comparison, and windowed sigma8 check.
- `environment/requirements.txt`: minimal Python dependencies.
- `manifests/`: file inventory, reproducibility notes, and a data availability statement template.

## Reproducing Figures And Tables

```bash
python -m pip install -r environment/requirements.txt
python scripts/build_all_figures.py
```

The scripts write generated outputs to `paper/figures/` and update the compressed S8 comparison table in `paper/tables/compressed_s8_comparison.tex`.

## Reproduce The Sigma8 Window Check

```bash
python scripts/build_sigma8_window_check.py
```

Outputs:

- `data/sigma8/sigma8_window_check.csv`
- `paper/tables/sigma8_window_check_table.tex`

## Manuscript Build

With a local LaTeX installation that includes REVTeX:

```bash
cd paper
latexmk -pdf paper.tex
```

If `latexmk` is unavailable, use the usual sequence:

```bash
pdflatex paper.tex
bibtex paper
pdflatex paper.tex
pdflatex paper.tex
```

## Data Availability

The CSV files in `data/` are the numerical inputs for the tables and figures. They are compressed release products, not a dump of the exploratory project directory.
The public repository is available at https://github.com/liyangmo730/selection-fold-dark-drain-class-benchmark.

## Citation

Please cite the manuscript and this repository. If an archival Zenodo DOI is added later, cite the DOI for the versioned release.
