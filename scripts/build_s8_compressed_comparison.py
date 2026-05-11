#!/usr/bin/env python3
"""Regenerate the compressed S8 comparison table and figure."""
from pathlib import Path
import math
import pandas as pd
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "s8_compressed"
OUT_TAB = ROOT / "paper" / "tables"
OUT_FIG = ROOT / "paper" / "figures"
OUT_TAB.mkdir(parents=True, exist_ok=True)
OUT_FIG.mkdir(parents=True, exist_ok=True)

S8_REF = 0.831
S8_REF_SIGMA = 0.013
SIGMA_THEORY = 0.015

branches = [
    {"branch": "Newtonian-gauge benchmark", "P_geo": 0.897145, "role": "main CLASS benchmark"},
    {"branch": "source-family B proxy", "P_geo": 0.896795, "role": "executable proxy control"},
    {"branch": "source-family D proxy", "P_geo": 0.896930, "role": "executable proxy candidate"},
]
observations = [
    {"dataset": "DES Y3 cosmic shear", "tex_dataset": "DES Y3 cosmic shear, $\\Lambda$CDM-optimized", "S8_obs": 0.772, "sigma_minus": 0.017, "sigma_plus": 0.018, "bibkey": "DESY3Shear"},
    {"dataset": "KiDS-1000 cosmic shear", "tex_dataset": "KiDS-1000 cosmic shear", "S8_obs": 0.759, "sigma_minus": 0.021, "sigma_plus": 0.024, "bibkey": "KiDS1000"},
    {"dataset": "HSC-Y3 cosmic shear", "tex_dataset": "HSC-Y3 cosmic shear", "S8_obs": 0.776, "sigma_minus": 0.033, "sigma_plus": 0.032, "bibkey": "HSCY3Shear"},
]

model_rows = []
for branch in branches:
    q = math.sqrt(branch["P_geo"])
    model_rows.append({
        "branch": branch["branch"],
        "role": branch["role"],
        "P_geo": branch["P_geo"],
        "sqrt_P_geo": q,
        "S8_ref": S8_REF,
        "S8_comp": S8_REF * q,
        "sigma_ref_prop": S8_REF_SIGMA * q,
        "sigma_theory": SIGMA_THEORY,
    })
model_df = pd.DataFrame(model_rows)

rows = []
for _, model in model_df.iterrows():
    for obs in observations:
        sigma_obs = 0.5 * (obs["sigma_minus"] + obs["sigma_plus"])
        sigma_total = math.sqrt(sigma_obs**2 + model["sigma_ref_prop"]**2 + SIGMA_THEORY**2)
        delta = model["S8_comp"] - obs["S8_obs"]
        rows.append({
            "branch": model["branch"],
            "dataset": obs["dataset"],
            "S8_comp": model["S8_comp"],
            "S8_obs": obs["S8_obs"],
            "sigma_obs_sym": sigma_obs,
            "sigma_total": sigma_total,
            "delta": delta,
            "pull_sigma": delta / sigma_total,
            "bibkey": obs["bibkey"],
        })
resid_df = pd.DataFrame(rows)
resid_df.to_csv(DATA / "compressed_s8_comparison.csv", index=False)

main_branch = model_df.iloc[0]
bs = chr(92)
tex_lines = [
    bs + "begin{table}[b]",
    bs + "centering",
    bs + "begin{tabular}{lccc}",
    bs + "toprule",
    "Compressed constraint & $S_8^{" + bs + "rm obs}$ & $S_8^{" + bs + "rm comp}$ & $" + bs + "Delta S_8$ " + bs + bs,
    bs + "midrule",
]
for obs in observations:
    sigma_obs = 0.5 * (obs["sigma_minus"] + obs["sigma_plus"])
    delta = main_branch["S8_comp"] - obs["S8_obs"]
    tex_lines.append(
        f"{obs['tex_dataset']}~{bs}cite{{{obs['bibkey']}}} & "
        f"${obs['S8_obs']:.3f}{bs}pm{sigma_obs:.3f}$ & "
        f"${main_branch['S8_comp']:.3f}$ & ${delta:+.3f}$ {bs}{bs}"
    )
tex_lines.extend([
    bs + "bottomrule",
    bs + "end{tabular}",
    bs + "caption{Compressed $S_8$ amplitude comparison for the fiducial Newtonian-gauge CLASS branch. The model value is computed as $S_{8}^{" + bs + "rm comp}=S_{8," + bs + "rm ref}" + bs + "sqrt{P_{" + bs + "rm geo}}$ using $S_{8," + bs + "rm ref}=0.831$. This is an amplitude-scale comparison only, not a weak-lensing, RSD, CMB, or combined likelihood analysis.}",
    bs + "label{tab:compressed_s8_comparison}",
    bs + "end{table}",
])
(OUT_TAB / "compressed_s8_comparison.tex").write_text(chr(10).join(tex_lines), encoding="utf-8")

labels = ["Planck ref."]
values = [S8_REF]
errors = [S8_REF_SIGMA]
for obs in observations:
    labels.append(obs["dataset"])
    values.append(obs["S8_obs"])
    errors.append(0.5 * (obs["sigma_minus"] + obs["sigma_plus"]))
for _, model in model_df.iterrows():
    labels.append(model["branch"])
    values.append(model["S8_comp"])
    errors.append(math.sqrt(model["sigma_ref_prop"]**2 + SIGMA_THEORY**2))

fig, ax = plt.subplots(figsize=(7.0, 4.2))
y = list(range(len(labels)))
ax.errorbar(values, y, xerr=errors, fmt="o", capsize=3)
ax.axvline(S8_REF, linestyle="--", linewidth=1)
ax.set_yticks(y)
ax.set_yticklabels(labels)
ax.invert_yaxis()
ax.set_xlabel("S8")
ax.set_title("Compressed S8 amplitude comparison")
ax.grid(True, axis="x", alpha=0.3)
fig.tight_layout()
fig.savefig(OUT_FIG / "compressed_s8_comparison.pdf")
fig.savefig(OUT_FIG / "compressed_s8_comparison.png", dpi=220)
plt.close(fig)
print(OUT_FIG / "compressed_s8_comparison.pdf")
