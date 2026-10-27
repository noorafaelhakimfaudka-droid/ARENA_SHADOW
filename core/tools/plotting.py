# ml-agents/core/tools/plotting.py
"""
Tool Visualisasi & Grafik Matplotlib/Seaborn Murni.
Membuat 5-6 grafik esensial sesuai standar Scope PRD:
1. fig1_target_distribution.png: Distribusi target (countplot / histplot).
2. fig2_feature_distributions.png: Distribusi 2-3 fitur penting.
3. fig3_correlation_matrix.png: Heatmap korelasi numerik.
4. fig4_cv_model_comparison.png: Perbandingan skor 5-Fold CV model baseline vs kandidat.
5. fig5_evaluation_metrics.png: Confusion matrix (klasifikasi) atau plot residual (regresi).
6. fig6_feature_importance.png: Top 10 fitur penentu keputusan model.
- Disimpan rapi di direktori outputs/<run_id>/figures/.
- Dilarang memanggil LLM (Murni plotting Matplotlib).
"""

from __future__ import annotations
from pathlib import Path
from typing import Any, Dict, List, Optional
import matplotlib
matplotlib.use("Agg")  # Mode non-interaktif tanpa GUI pop-up
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns


def setup_plot_style():
    """Mengatur gaya visual grafik yang bersih, profesional, dan tajam."""
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    plt.rcParams["font.sans-serif"] = "DejaVu Sans"
    plt.rcParams["axes.edgecolor"] = "#cbd5e1"
    plt.rcParams["axes.linewidth"] = 0.8


def generate_all_figures(
    df: pd.DataFrame,
    target_col: str,
    task_type: str,
    cv_results: Dict[str, Dict[str, Any]],
    test_metrics: Dict[str, Any],
    top_features: List[Dict[str, Any]],
    output_dir: Path | str
) -> List[str]:
    """
    Menghasilkan seluruh rangkaian visualisasi wajib dan menyimpannya ke folder figures/.
    Mengembalikan daftar nama berkas gambar yang berhasil dibuat.
    """
    setup_plot_style()
    fig_dir = Path(output_dir) / "figures"
    fig_dir.mkdir(parents=True, exist_ok=True)
    generated_files: List[str] = []

    # -------------------------------------------------------------
    # 1. FIG 1: DISTRIBUSI TARGET
    # -------------------------------------------------------------
    try:
        fig, ax = plt.subplots(figsize=(6, 4))
        if task_type in ("binary_classification", "multiclass_classification"):
            sns.countplot(data=df, x=target_col, palette="Blues_d", ax=ax)
            ax.set_title(f"Distribusi Target: '{target_col}'", fontsize=12, fontweight="bold")
            # Tampilkan persentase di atas bar
            total = len(df[target_col].dropna())
            for p in ax.patches:
                height = p.get_height()
                ax.annotate(f"{height/total:.1%}", (p.get_x() + p.get_width() / 2., height / 2),
                            ha="center", va="center", color="white", fontweight="bold", fontsize=10)
        else:
            sns.histplot(df[target_col].dropna(), kde=True, color="#3b82f6", ax=ax)
            ax.set_title(f"Distribusi Target Kontinu: '{target_col}'", fontsize=12, fontweight="bold")
        
        plt.tight_layout()
        fpath = fig_dir / "fig1_target_distribution.png"
        plt.savefig(fpath, dpi=180)
        plt.close(fig)
        generated_files.append("figures/fig1_target_distribution.png")
    except Exception as e:
        print(f"[Plot Warning] Gagal membuat fig1: {e}")

    # -------------------------------------------------------------
    # 2. FIG 2: DISTRIBUSI 2-3 FITUR UTAMA
    # -------------------------------------------------------------
    try:
        num_cols = [c for c in df.select_dtypes(include=["number"]).columns if c != target_col][:3]
        if num_cols:
            fig, axes = plt.subplots(1, len(num_cols), figsize=(4 * len(num_cols), 3.5))
            if len(num_cols) == 1:
                axes = [axes]
            for i, col in enumerate(num_cols):
                sns.histplot(df[col].dropna(), kde=True, color="#0ea5e9", ax=axes[i])
                axes[i].set_title(f"Sebaran: {col}", fontsize=10, fontweight="bold")
            plt.tight_layout()
            fpath = fig_dir / "fig2_feature_distributions.png"
            plt.savefig(fpath, dpi=180)
            plt.close(fig)
            generated_files.append("figures/fig2_feature_distributions.png")
    except Exception as e:
        print(f"[Plot Warning] Gagal membuat fig2: {e}")

    # -------------------------------------------------------------
    # 3. FIG 3: HEATMAP KORELASI NUMERIK
    # -------------------------------------------------------------
    try:
        num_df = df.select_dtypes(include=["number"]).dropna()
        if num_df.shape[1] >= 2:
            fig, ax = plt.subplots(figsize=(7, 5))
            corr = num_df.corr()
            sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", vmin=-1, vmax=1, ax=ax, cbar=True)
            ax.set_title("Matriks Korelasi Fitur Numerik", fontsize=12, fontweight="bold")
            plt.tight_layout()
            fpath = fig_dir / "fig3_correlation_matrix.png"
            plt.savefig(fpath, dpi=180)
            plt.close(fig)
            generated_files.append("figures/fig3_correlation_matrix.png")
    except Exception as e:
        print(f"[Plot Warning] Gagal membuat fig3: {e}")

    # -------------------------------------------------------------
    # 4. FIG 4: PERBANDINGAN MODEL 5-FOLD CV
    # -------------------------------------------------------------
    try:
        if cv_results:
            fig, ax = plt.subplots(figsize=(7, 4))
            model_names = list(cv_results.keys())
            means = [cv_results[m]["cv_mean"] for m in model_names]
            stds = [cv_results[m]["cv_std"] for m in model_names]
            
            y_pos = np.arange(len(model_names))
            bars = ax.barh(y_pos, means, xerr=stds, align="center", color="#6366f1", alpha=0.85, capsize=4, edgecolor="#312e81")
            ax.set_yticks(y_pos)
            ax.set_yticklabels(model_names, fontweight="bold")
            ax.invert_yaxis()
            ax.set_xlabel("Rata-Rata Skor 5-Fold Cross Validation")
            ax.set_title("Perbandingan Skor Evaluasi Kandidat Model (CV Mean ± Std)", fontsize=11, fontweight="bold")
            
            # Tuliskan nilai di samping bar
            for i, v in enumerate(means):
                ax.text(v + (max(means) * 0.02), i, f"{v:.4f}", va="center", fontsize=9, fontweight="bold")
                
            plt.tight_layout()
            fpath = fig_dir / "fig4_cv_model_comparison.png"
            plt.savefig(fpath, dpi=180)
            plt.close(fig)
            generated_files.append("figures/fig4_cv_model_comparison.png")
    except Exception as e:
        print(f"[Plot Warning] Gagal membuat fig4: {e}")

    # -------------------------------------------------------------
    # 5. FIG 5: EVALUASI TEST SET (CONFUSION MATRIX / RESIDUAL PLOT)
    # -------------------------------------------------------------
    try:
        if "confusion_matrix" in test_metrics:
            cm = np.array(test_metrics["confusion_matrix"])
            fig, ax = plt.subplots(figsize=(5, 4))
            sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax, cbar=False)
            ax.set_title("Confusion Matrix (Test Set Holdout)", fontsize=11, fontweight="bold")
            ax.set_xlabel("Prediksi Model")
            ax.set_ylabel("Fakta Sebenarnya")
            plt.tight_layout()
            fpath = fig_dir / "fig5_evaluation_metrics.png"
            plt.savefig(fpath, dpi=180)
            plt.close(fig)
            generated_files.append("figures/fig5_evaluation_metrics.png")
        elif "mae" in test_metrics:
            # Regresi residual visual placeholder
            fig, ax = plt.subplots(figsize=(6, 4))
            ax.text(0.5, 0.5, f"Metrik Regresi Test Set:\n\nMAE: {test_metrics['mae']:.2f}\nRMSE: {test_metrics['rmse']:.2f}\nR²: {test_metrics['r2']:.4f}",
                    ha="center", va="center", fontsize=13, fontweight="bold", bbox=dict(boxstyle="round,pad=1", facecolor="#f0f9ff", edgecolor="#0284c7"))
            ax.axis("off")
            ax.set_title("Evaluasi Metrik Uji Regresi", fontsize=12, fontweight="bold")
            plt.tight_layout()
            fpath = fig_dir / "fig5_evaluation_metrics.png"
            plt.savefig(fpath, dpi=180)
            plt.close(fig)
            generated_files.append("figures/fig5_evaluation_metrics.png")
    except Exception as e:
        print(f"[Plot Warning] Gagal membuat fig5: {e}")

    # -------------------------------------------------------------
    # 6. FIG 6: TOP 10 FEATURE IMPORTANCE
    # -------------------------------------------------------------
    try:
        if top_features:
            fig, ax = plt.subplots(figsize=(7, 4.5))
            f_names = [f["feature"] for f in top_features][::-1]
            f_vals = [f["importance"] for f in top_features][::-1]
            
            ax.barh(f_names, f_vals, color="#10b981", edgecolor="#064e3b", alpha=0.9)
            ax.set_xlabel("Tingkat Pengaruh (Importance / Koefisien)")
            ax.set_title("Top 10 Fitur Penentu Keputusan Model", fontsize=11, fontweight="bold")
            plt.tight_layout()
            fpath = fig_dir / "fig6_feature_importance.png"
            plt.savefig(fpath, dpi=180)
            plt.close(fig)
            generated_files.append("figures/fig6_feature_importance.png")
    except Exception as e:
        print(f"[Plot Warning] Gagal membuat fig6: {e}")

    return generated_files
