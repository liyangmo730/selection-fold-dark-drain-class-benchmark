#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data" / "matter_power_dense"
OUT_DIR = ROOT / "data" / "sigma8"
TABLE_DIR = ROOT / "paper" / "tables"
OUT_DIR.mkdir(parents=True, exist_ok=True)
TABLE_DIR.mkdir(parents=True, exist_ok=True)

FILES = {
    "reference": DATA_DIR / "reference_pk_z0.dat",
    "Newtonian-gauge benchmark": DATA_DIR / "newtonian_benchmark_pk_z0.dat",
    "drain-only": DATA_DIR / "drain_only_pk_z0.dat",
    "B proxy": DATA_DIR / "source_B_proxy_pk_z0.dat",
    "D proxy": DATA_DIR / "source_D_proxy_pk_z0.dat",
}
R8 = 8.0

def read_pk(path):
    arr = np.loadtxt(path)
    if arr.ndim != 2 or arr.shape[1] < 2:
        raise ValueError(f"Expected at least two columns in {path}")
    k = arr[:, 0]
    pk = arr[:, 1]
    m = np.isfinite(k) & np.isfinite(pk) & (k > 0) & (pk > 0)
    k, pk = k[m], pk[m]
    order = np.argsort(k)
    return k[order], pk[order]

def W_tophat(x):
    x = np.asarray(x, dtype=float)
    out = np.empty_like(x)
    small = np.abs(x) < 1e-4
    xs = x[small]
    out[small] = 1 - xs**2/10 + xs**4/280
    xn = x[~small]
    out[~small] = 3 * (np.sin(xn) - xn*np.cos(xn)) / xn**3
    return out

def sigma8_sq(k, pk):
    w = W_tophat(k * R8)
    integrand = k**2 * pk * w**2
    return np.trapezoid(integrand, k) / (2*np.pi**2)

def pgeo_ratio(k_ref, pk_ref, k_model, pk_model, kmin=None, kmax=None):
    pk_interp = np.interp(k_ref, k_model, pk_model)
    ratio = pk_interp / pk_ref
    mask = np.ones_like(k_ref, dtype=bool)
    if kmin is not None:
        mask &= k_ref >= kmin
    if kmax is not None:
        mask &= k_ref <= kmax
    return np.exp(np.mean(np.log(ratio[mask])))

if not FILES["reference"].exists():
    raise FileNotFoundError(f"Missing reference file: {FILES['reference']}")

k_ref, pk_ref = read_pk(FILES["reference"])
sig8_ref_sq = sigma8_sq(k_ref, pk_ref)
rows = []
for branch, path in FILES.items():
    if not path.exists():
        print(f"SKIP missing: {path}")
        continue
    k, pk = read_pk(path)
    pk_on_ref = np.interp(k_ref, k, pk)
    sig8_sq_val = sigma8_sq(k_ref, pk_on_ref)
    sig8_ratio = np.sqrt(sig8_sq_val / sig8_ref_sq)
    ratio_dense = pk_on_ref / pk_ref
    pgeo_dense = np.exp(np.mean(np.log(ratio_dense)))
    sqrt_pgeo_dense = np.sqrt(pgeo_dense)
    pgeo_band = pgeo_ratio(k_ref, pk_ref, k, pk, kmin=0.01, kmax=0.30)
    sqrt_pgeo_band = np.sqrt(pgeo_band)
    tilt_geo = 100 * np.max(np.abs(ratio_dense / pgeo_dense - 1))
    rows.append({
        "branch": branch,
        "P_geo_dense": pgeo_dense,
        "sqrt_P_geo_dense": sqrt_pgeo_dense,
        "P_geo_0p01_0p30": pgeo_band,
        "sqrt_P_geo_0p01_0p30": sqrt_pgeo_band,
        "sigma8_ratio": sig8_ratio,
        "sigma8_minus_sqrt_Pgeo_dense": sig8_ratio - sqrt_pgeo_dense,
        "sigma8_minus_sqrt_Pgeo_band": sig8_ratio - sqrt_pgeo_band,
        "tilt_dense_percent": tilt_geo,
        "k_min": float(k_ref.min()),
        "k_max": float(k_ref.max()),
        "n_k": int(len(k_ref)),
    })

df = pd.DataFrame(rows)
csv_path = OUT_DIR / "sigma8_window_check.csv"
df.to_csv(csv_path, index=False)

tex = []
tex.append(r"\begin{table}[t]")
tex.append(r"\centering")
tex.append(r"\begin{tabular}{lcccc}")
tex.append(r"\toprule")
tex.append(r"Branch & $\sqrt{P_{\rm geo}}$ & $\sigma_8/\sigma_{8,\rm ref}$ & Difference & Note \\")
tex.append(r"\midrule")
for _, r in df.iterrows():
    note = "reference" if r["branch"] == "reference" else "windowed check"
    tex.append(
        f"{r['branch']} & "
        f"${r['sqrt_P_geo_0p01_0p30']:.6f}$ & "
        f"${r['sigma8_ratio']:.6f}$ & "
        f"${r['sigma8_minus_sqrt_Pgeo_band']:+.3e}$ & "
        f"{note} " + r"\\"
    )
tex.append(r"\bottomrule")
tex.append(r"\end{tabular}")
tex.append(
    r"\caption{Windowed $\sigma_8$ amplitude check from dense $z=0$ matter-power arrays. "
    r"The $\sqrt{P_{\rm geo}}$ column uses the same $k=0.01$--$0.30\,h\,{\rm Mpc}^{-1}$ "
    r"band used in the benchmark summaries, while $\sigma_8/\sigma_{8,\rm ref}$ is computed "
    r"with the top-hat window. This is an amplitude check only, not a likelihood analysis.}"
)
tex.append(r"\label{tab:sigma8_window_check}")
tex.append(r"\end{table}")
tex_path = TABLE_DIR / "sigma8_window_check_table.tex"
tex_path.write_text("\n".join(tex), encoding="utf-8")
print(df.to_string(index=False))
print(f"Wrote {csv_path}")
print(f"Wrote {tex_path}")
