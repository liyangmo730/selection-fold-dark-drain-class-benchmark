#!/usr/bin/env python3
"""Regenerate manuscript figures from the curated release data."""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
FIG = ROOT / "paper" / "figures"
FIG.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({
    "font.size": 10,
    "axes.labelsize": 10,
    "axes.titlesize": 11,
    "legend.fontsize": 8,
    "figure.dpi": 160,
    "savefig.dpi": 220,
})


def savefig(name):
    path = FIG / name
    plt.tight_layout()
    plt.savefig(path, bbox_inches="tight")
    plt.close()
    print(path)


def fig1_mechanism():
    labels = [
        "selection\npotential",
        "fold\ntransition",
        "scalar\nentrainment",
        "CDM mass\nmodulation",
        "late-time\nCDM drain",
        "lower\nP(k), S8",
    ]
    fig, ax = plt.subplots(figsize=(8.8, 2.2))
    ax.set_axis_off()
    xs = np.linspace(0.08, 0.92, len(labels))
    y = 0.55
    for i, (x, lab) in enumerate(zip(xs, labels)):
        box = FancyBboxPatch(
            (x - 0.065, y - 0.14), 0.13, 0.28,
            boxstyle="round,pad=0.025,rounding_size=0.02",
            linewidth=1.1, facecolor="#edf3ff", edgecolor="#355c9a",
        )
        ax.add_patch(box)
        ax.text(x, y, lab, ha="center", va="center")
        if i < len(labels) - 1:
            ax.add_patch(FancyArrowPatch(
                (x + 0.07, y), (xs[i + 1] - 0.07, y),
                arrowstyle="->", mutation_scale=12, linewidth=1.1,
                color="#333333",
            ))
    ax.text(0.5, 0.15, "late-time selection-fold dark-drain chain",
            ha="center", va="center", color="#444444")
    savefig("fig1_mechanism.pdf")


def fig2_background():
    bg = pd.read_csv(DATA / "background" / "background_bridge.csv")
    z_all = bg["z"].to_numpy()
    mask = (z_all >= 0) & (z_all <= 5)
    z = z_all[mask]
    rel = bg["H_over_Hrecon_minus_one"].to_numpy()[mask]
    source = bg["drain_source"].to_numpy()[mask]
    transfer = bg["d_transfer"].to_numpy()[mask]
    order = np.argsort(z)
    z, rel, source, transfer = [a[order] for a in (z, rel, source, transfer)]

    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.2))
    axes[0].plot(z, rel, color="#1f77b4", lw=1.6)
    axes[0].axhline(0, color="k", lw=0.7)
    axes[0].set_xlabel("z")
    axes[0].set_ylabel("H_CLASS/H_recon - 1")
    axes[0].set_title("background handoff residual")
    axes[0].set_xlim(0, 5)
    axes[0].set_ylim(-8e-4, 8e-4)

    axes[1].plot(z, source / max(np.max(np.abs(source)), 1e-30),
                 label="Gamma_drain Omega_c (norm.)", color="#d62728", lw=1.5)
    axes[1].plot(z, transfer / max(np.max(np.abs(transfer)), 1e-30),
                 label="d_transfer (norm.)", color="#2ca02c", lw=1.5)
    axes[1].set_xlabel("z")
    axes[1].set_title("drain activation diagnostics")
    axes[1].set_xlim(0, 3)
    axes[1].legend(frameon=False)
    savefig("fig2_background_bridge.pdf")


def fig3_pk_redshift():
    df = pd.read_csv(DATA / "matter_power" / "source_layer_redshift_summary.csv")
    fig, ax = plt.subplots(figsize=(5.7, 3.6))
    ax.plot(df["z"], df["conservative"], "o-", label="conservative")
    ax.plot(df["z"], df["mild_k_dependent"], "s-", label="mild k-dependent")
    ax.plot(df["z"], df["boundary"], "^-", label="boundary")
    ax.axhline(1, color="k", lw=0.8, ls="--")
    ax.set_xlabel("z")
    ax.set_ylabel("P/P_off")
    ax.set_title("redshift relaxation of source-layer suppression")
    ax.set_ylim(0.935, 1.005)
    ax.legend(frameon=False)
    savefig("fig3_pk_redshift.pdf")


def fig4_dynamic_response():
    curves = pd.read_csv(DATA / "response" / "dynamic_response_curves.csv").sort_values("z")
    comp = pd.read_csv(DATA / "response" / "dynamic_response_summary.csv")
    robust = comp[comp["case"].str.contains("robust", case=False)].iloc[0]

    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.2))
    axes[0].plot(curves["z"], curves["eta_x_qs"], label="R_x QS", lw=1.5)
    axes[0].plot(curves["z"], curves["eta_x_dyn"], label="eta_x dyn", lw=1.5)
    axes[0].invert_xaxis()
    axes[0].set_xlabel("z")
    axes[0].set_ylabel("response amplitude")
    axes[0].set_title("dynamic vs QS response (k=0.1)")
    axes[0].legend(frameon=False)

    vals = [
        robust["dyn_minus_QS_ratio_min_all_z"],
        robust["dyn_minus_QS_response_share_z0"],
        robust["dyn_minus_QS_tilt"],
    ]
    axes[1].bar(["power floor", "response share", "tilt"], vals,
                color=["#4c78a8", "#f58518", "#54a24b"])
    axes[1].axhline(0, color="k", lw=0.8)
    axes[1].set_title("dynamic minus QS shifts")
    axes[1].tick_params(axis="x", rotation=20)
    savefig("fig4_dynamic_response.pdf")


def fig5_newtonian():
    data = pd.read_csv(DATA / "matter_power" / "newtonian_benchmark_branches.csv")
    x = np.arange(len(data))
    y = data["P_geo_vs_metric_off"].to_numpy()
    yerr = np.vstack([y - data["P_min"].to_numpy(), data["P_max"].to_numpy() - y])
    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    ax.errorbar(x, y, yerr=yerr, fmt="o", capsize=4, color="#1f77b4")
    ax.axhline(1, color="k", lw=0.8, ls="--")
    ax.set_xticks(x)
    ax.set_xticklabels(data["branch_label"], rotation=20, ha="right")
    ax.set_ylabel("P_geo")
    ax.set_title("Newtonian-gauge CLASS benchmark and proxy branches")
    ax.set_ylim(0.84, 1.02)
    savefig("fig5_newtonian_readiness.pdf")


def fig6_s8_ladder():
    s8 = pd.read_csv(DATA / "s8_compressed" / "s8_proxy_table.csv")
    fig, ax = plt.subplots(figsize=(6.8, 3.6))
    ax.bar(s8["branch_label"], s8["S8_suppression_pct_proxy"], color="#6a9fb5")
    ax.axhspan(4.5, 6.0, color="#d9ead3", alpha=0.5, label="few-percent target scale")
    ax.set_ylabel("1 - sqrt(P_geo) (%)")
    ax.set_title("S8-facing proxy amplitude ladder")
    ax.set_ylim(0, 6.5)
    ax.legend(frameon=False, loc="upper right")
    savefig("fig6_s8_proxy_ladder.pdf")


def main():
    fig1_mechanism()
    fig2_background()
    fig3_pk_redshift()
    fig4_dynamic_response()
    fig5_newtonian()
    fig6_s8_ladder()


if __name__ == "__main__":
    main()
