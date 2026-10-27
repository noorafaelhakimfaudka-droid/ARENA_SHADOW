import logging
from pathlib import Path
from typing import Any, Dict, List, Tuple
import nbformat as nbf
from nbclient import NotebookClient

from backend.app.schemas import ProblemSpec, Round

logger = logging.getLogger("shadow_arena.notebook")


def generate_notebook_cells(
    csv_filename: str,
    problem: ProblemSpec,
    rounds: List[Round],
    ml_results: Dict[str, Any]
) -> nbf.NotebookNode:
    """
    Menghasilkan objek notebook nbformat yang berisi kode pipeline ML nyata,
    lengkap dengan narasi markdown dari hasil debat 5 agen.
    """
    nb = nbf.v4.new_notebook()
    nb.metadata = {
        "kernelspec": {
            "display_name": "Python 3 (ipykernel)",
            "language": "python",
            "name": "python3"
        },
        "language_info": {
            "name": "python",
            "version": "3.11"
        }
    }

    cells = []

    # 1. Title cell
    title_md = (
        f"# Shadow Arena — Notebook Riset & Audit ML\n"
        f"Dataset: **{csv_filename}** | Target: **{problem.target}** ({problem.task})\n\n"
        f"Notebook ini dirakit otomatis oleh **NOTEBOOK BUILDER** dari hasil debat 5 agen AI "
        f"berdasarkan komputasi faktual dan pipeline auditable."
    )
    cells.append(nbf.v4.new_markdown_cell(title_md))

    # 2. Imports & Setup
    setup_code = (
        "import numpy as np\n"
        "import pandas as pd\n"
        "import matplotlib.pyplot as plt\n"
        "import joblib\n"
        "from scipy import stats\n"
        "from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score, learning_curve\n"
        "from sklearn.compose import ColumnTransformer\n"
        "from sklearn.pipeline import Pipeline\n"
        "from sklearn.impute import SimpleImputer\n"
        "from sklearn.preprocessing import StandardScaler, OneHotEncoder\n"
        "from sklearn.dummy import DummyClassifier\n"
        "from sklearn.linear_model import LogisticRegression\n"
        "from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier\n"
        "from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, roc_curve\n"
        "from sklearn.inspection import permutation_importance\n\n"
        "# Pengaturan tampilan plot\n"
        "plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')\n"
        "print('Semua pustaka berhasil dimuat.')"
    )
    cells.append(nbf.v4.new_code_cell(setup_code))

    # 3. Load Data
    load_code = (
        f"df = pd.read_csv('raw.csv')\n"
        f"TARGET = '{problem.target}'\n"
        f"print(f'Dimensi dataset: {{df.shape[0]}} baris, {{df.shape[1]}} kolom.')\n"
        f"df.head(3)"
    )
    cells.append(nbf.v4.new_code_cell(load_code))

    # Sisipkan sel per babak debat
    for r in rounds:
        # Markdown perdebatan agen
        agent_md = (
            f"### {r.title}\n"
            f"> **{r.agent.upper()}** [{r.mood.upper()}]: {r.dialog}\n\n"
            f"`Bukti Audit: {r.evidence}`"
        )
        cells.append(nbf.v4.new_markdown_cell(agent_md))

        # Kode Python yang sesuai dengan tahapan
        code_str = ""
        if r.stage == "PROBLEM":
            code_str = (
                f"print('Problem Task:', '{problem.task}')\n"
                f"print('Target Distribution:')\n"
                f"print(df[TARGET].value_counts(normalize=True))"
            )
        elif r.stage == "DATA" and "understanding" in r.title.lower():
            code_str = (
                "print('Missing Values per Kolom:')\n"
                "print(df.isna().mean().sort_values(ascending=False).head(5))"
            )
        elif r.stage == "DATA" and "cleaning" in r.title.lower():
            code_str = (
                "df_clean = df.drop_duplicates().copy()\n"
                "# Saring kolom yang kosong lebih dari 60%\n"
                "valid_cols = df_clean.columns[df_clean.isna().mean() <= 0.6]\n"
                "df_clean = df_clean[valid_cols]\n"
                "print(f'Kolom tersisa: {len(df_clean.columns)}')\n"
                "df_clean.shape"
            )
        elif r.stage == "SPLIT_FE" and "split" in r.title.lower():
            code_str = (
                "clean_sub = df.dropna(subset=[TARGET]).copy()\n"
                "y = clean_sub[TARGET]\n"
                "X = clean_sub.drop(columns=[TARGET])\n"
                "y_enc, class_names = pd.factorize(y, sort=True)\n"
                "y_enc = pd.Series(y_enc, index=clean_sub.index)\n"
                "X_tr, X_te, y_tr, y_te = train_test_split(X, y_enc, test_size=0.2, stratify=y_enc, random_state=42)\n"
                "print(f'Train set: {len(X_tr)} baris | Test set terkunci: {len(X_te)} baris')"
            )
        elif r.stage == "SPLIT_FE" and "fitur" in r.title.lower():
            code_str = (
                "for d in (X_tr, X_te):\n"
                "    if {'sibsp', 'parch'}.issubset(set(d.columns)):\n"
                "        d['family_size'] = d['sibsp'] + d['parch'] + 1\n"
                "        d['is_alone'] = (d['family_size'] == 1).astype(int)\n"
                "print('Rekayasa fitur selesai. Kolom train:', list(X_tr.columns[:6]))"
            )
        elif r.stage == "SPLIT_FE" and "kebocoran" in r.title.lower():
            code_str = (
                "# Deteksi korelasi tinggi dengan target\n"
                "num_c = X_tr.select_dtypes(include=[np.number]).columns\n"
                "corrs = {}\n"
                "for c in num_c:\n"
                "    val = abs(np.corrcoef(X_tr[c].fillna(X_tr[c].median()), y_tr)[0, 1])\n"
                "    if not np.isnan(val):\n"
                "        corrs[c] = val\n"
                "leaks = [c for c, r in corrs.items() if r > 0.85]\n"
                "print('Kolom bocor (|r| > 0.85):', leaks)\n"
                "if leaks:\n"
                "    X_tr = X_tr.drop(columns=leaks)\n"
                "    X_te = X_te.drop(columns=leaks)"
            )
        elif r.stage == "MODEL" and "kandidat" in r.title.lower():
            code_str = (
                "num_cols = X_tr.select_dtypes(include=[np.number]).columns.tolist()\n"
                "cat_cols = [c for c in X_tr.columns if c not in num_cols]\n"
                "preprocessor = ColumnTransformer([\n"
                "    ('num', Pipeline([('imp', SimpleImputer(strategy='median')), ('sc', StandardScaler())]), num_cols),\n"
                "    ('cat', Pipeline([('imp', SimpleImputer(strategy='most_frequent')), ('ohe', OneHotEncoder(handle_unknown='ignore', sparse_output=False))]), cat_cols)\n"
                "])\n"
                "models = {\n"
                "    'Dummy': DummyClassifier(strategy='prior'),\n"
                "    'Logistic Regression L2': LogisticRegression(max_iter=1000, random_state=42),\n"
                "    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),\n"
                "    'Gradient Boosting': GradientBoostingClassifier(random_state=42)\n"
                "}\n"
                "pipes = {name: Pipeline([('prep', preprocessor), ('m', m)]) for name, m in models.items()}\n"
                "cv = StratifiedKFold(5, shuffle=True, random_state=42)\n"
                "for name, p in pipes.items():\n"
                "    sc = cross_val_score(p, X_tr, y_tr, cv=cv, scoring='roc_auc')\n"
                "    print(f'{name}: {sc.mean():.3f} ± {sc.std():.3f}')"
            )
        elif r.stage == "MODEL" and "overfit" in r.title.lower():
            code_str = (
                "best_pipe = pipes['Logistic Regression L2']\n"
                "sizes, tr_s, va_s = learning_curve(best_pipe, X_tr, y_tr, cv=cv, scoring='roc_auc', train_sizes=np.linspace(0.2, 1.0, 5))\n"
                "print(f'Train mean: {tr_s.mean(axis=1)[-1]:.3f} | Valid mean: {va_s.mean(axis=1)[-1]:.3f}')\n"
                "print(f'Gap train-valid: {tr_s.mean(axis=1)[-1] - va_s.mean(axis=1)[-1]:.3f}')"
            )
        elif r.stage == "MODEL" and "kanari" in r.title.lower():
            code_str = (
                "# Uji Kanari: Label diacak\n"
                "rng = np.random.default_rng(42)\n"
                "y_shuf = pd.Series(rng.permutation(y_tr.values), index=y_tr.index)\n"
                "c_sc = cross_val_score(best_pipe, X_tr, y_shuf, cv=cv, scoring='roc_auc')\n"
                "print(f'Kanari (label diacak) ROC-AUC: {c_sc.mean():.3f} (mendekati 0.50)')\n\n"
                "# Uji Derau 15% pada fitur numerik\n"
                "X_n = X_tr.copy()\n"
                "for c in num_cols:\n"
                "    std_val = X_n[c].std() or 1.0\n"
                "    X_n[c] = X_n[c] + rng.normal(0, 0.15 * std_val, size=len(X_n))\n"
                "for name in ['Logistic Regression L2', 'Gradient Boosting']:\n"
                "    n_sc = cross_val_score(pipes[name], X_n, y_tr, cv=cv, scoring='roc_auc')\n"
                "    print(f'{name} dengan derau 15%: {n_sc.mean():.3f}')"
            )
        elif r.stage == "EVAL" and "signifikansi" in r.title.lower():
            code_str = (
                "s_gb = cross_val_score(pipes['Gradient Boosting'], X_tr, y_tr, cv=cv, scoring='roc_auc')\n"
                "s_lr = cross_val_score(pipes['Logistic Regression L2'], X_tr, y_tr, cv=cv, scoring='roc_auc')\n"
                "d = s_gb - s_lr\n"
                "k = len(d)\n"
                "t_stat = d.mean() / np.sqrt(((1/k) + 0.25) * d.var(ddof=1))\n"
                "p_val = 2 * stats.t.sf(abs(t_stat), df=k - 1)\n"
                "print(f'Nadeau-Bengio corrected t-test p-value: {p_val:.3f}')\n"
                "if p_val >= 0.05:\n"
                "    print('Hasil: Perbedaan tidak signifikan (p >= 0.05). Memilih Logistic Regression L2.')\n"
                "else:\n"
                "    print('Hasil: Perbedaan signifikan (p < 0.05).')"
            )
        elif r.stage == "EVAL" and "akhir" in r.title.lower():
            code_str = (
                "champion = pipes['Logistic Regression L2'].fit(X_tr, y_tr)\n"
                "y_prob = champion.predict_proba(X_te)[:, 1]\n"
                "test_auc = roc_auc_score(y_te, y_prob)\n"
                "print(f'Hasil Akhir di Test Set Terkunci ROC-AUC: {test_auc:.3f}')\n"
                "print(classification_report(y_te, (y_prob >= 0.5).astype(int)))"
            )
        elif r.stage == "INSIGHT" and "temuan" in r.title.lower():
            code_str = (
                "tmp = pd.concat([X_tr, y_tr.rename('target')], axis=1)\n"
                "if 'sex' in tmp.columns:\n"
                "    print('Target Rate per Sex:')\n"
                "    print(tmp.groupby('sex')['target'].mean().round(3) * 100)"
            )
        elif r.stage == "INSIGHT" and "storytelling" in r.title.lower():
            code_str = (
                "imp = permutation_importance(champion, X_te, y_te, scoring='roc_auc', n_repeats=10, random_state=42)\n"
                "feat_imp = pd.Series(imp.importances_mean, index=X_te.columns).sort_values(ascending=False)\n"
                "print('Top 5 Fitur Terpenting (Permutasi):')\n"
                "print(feat_imp.head(5))"
            )
        elif r.stage == "NOTEBOOK":
            code_str = (
                "joblib.dump(champion, 'model_final.joblib')\n"
                "print('Model final disimpan ke model_final.joblib siap produksi.')"
            )

        if code_str:
            cells.append(nbf.v4.new_code_cell(code_str))

    nb.cells = cells
    return nb


def build_and_execute_notebook(
    session_dir: Path,
    csv_filename: str,
    problem: ProblemSpec,
    rounds: List[Round],
    ml_results: Dict[str, Any]
) -> Tuple[Path, bool, int]:
    """
    Membangun notebook .ipynb, memvalidasi skema dengan nbformat,
    dan mengeksekusinya secara nyata menggunakan nbclient (timeout 120s).
    """
    nb = generate_notebook_cells(csv_filename, problem, rounds, ml_results)

    # Validasi struktur
    try:
        nbf.validate(nb)
    except Exception as e:
        logger.error(f"Validasi skema notebook gagal: {str(e)}")
        out_path = session_dir / "shadow_arena.ipynb"
        with open(out_path, "w", encoding="utf-8") as f:
            nbf.write(nb, f)
        return out_path, False, len(nb.cells)

    # Eksekusi notebook
    out_path = session_dir / "shadow_arena.ipynb"
    is_valid = False

    try:
        client = NotebookClient(nb, timeout=120, kernel_name="python3", resources={"metadata": {"path": str(session_dir)}})
        client.execute()
        is_valid = True
        logger.info(f"Notebook dieksekusi sukses ({len(nb.cells)} sel).")
    except Exception as e:
        logger.warning(f"Eksekusi notebook menghasilkan warning/error: {str(e)[:150]}. Menyimpan notebook dengan catatan.")
        is_valid = False

    with open(out_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)

    return out_path, is_valid, len(nb.cells)
