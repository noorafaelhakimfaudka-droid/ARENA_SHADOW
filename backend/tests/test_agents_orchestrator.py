import json
from pathlib import Path
import pytest

from backend.app.services.validators import (
    extract_numbers_from_text,
    extract_numbers_from_facts,
    validate_dialogue,
)
from backend.app.services.agents.framer import ProblemFramer
from backend.app.services.agents.wrangler import DataWrangler
from backend.app.services.agents.guardian import ModelGuardian
from backend.app.services.agents.storyteller import InsightStoryteller
from backend.app.services.agents.notebook import NotebookAgent
from backend.app.schemas import DebateDocument


def test_validators_number_extraction_and_rejection():
    facts = {
        "n_rows": 891,
        "class_0_pct": 62,
        "class_1_pct": 38,
        "cv_auc": 0.868,
        "gap": 0.026
    }
    
    # Dialog dengan angka yang ada di fakta
    title_valid = "Problem Statement"
    dialog_valid = "Data ini memiliki 891 baris dengan kelas 62% dan 38%. Gap cuma 0.026."
    is_valid, errors = validate_dialogue(title_valid, dialog_valid, facts)
    assert is_valid is True
    assert len(errors) == 0

    # Dialog dengan angka halusinasi
    dialog_hallucinated = "Data ini memiliki 9999 baris dengan akurasi 99%."
    is_valid, errors = validate_dialogue(title_valid, dialog_hallucinated, facts)
    assert is_valid is False
    assert any("9999" in e or "99" in e for e in errors)


def test_validators_length_limits():
    facts = {"test": 123}
    title_too_long = "Judul Babak Ini Terlalu Panjang Dan Melebihi Batas 28 Karakter"
    dialog_ok = "Dialog pendek dan aman."
    is_valid, errors = validate_dialogue(title_too_long, dialog_ok, facts)
    assert is_valid is False
    assert any("Title melebihi batas 28 karakter" in e for e in errors)

    title_ok = "Judul Pendek"
    dialog_too_long = "A" * 195
    is_valid, errors = validate_dialogue(title_ok, dialog_too_long, facts)
    assert is_valid is False
    assert any("Dialog melebihi batas 190 karakter" in e for e in errors)


def test_agent_offline_dialogues_length_and_numbers():
    framer = ProblemFramer()
    wrangler = DataWrangler()
    guardian = ModelGuardian()
    storyteller = InsightStoryteller()
    notebook = NotebookAgent()

    test_facts = {
        "dataset_name": "titanic.csv",
        "target": "survived",
        "task": "klasifikasi biner",
        "class_0_pct": 62,
        "class_1_pct": 38,
        "metric": "ROC-AUC",
        "n_rows": 891,
        "n_cols": 12,
        "n_train": 712,
        "n_test": 179,
        "vif_max": 2.6,
        "dummy_score": 0.500,
        "logreg_score": 0.782,
        "rf_score": 0.851,
        "gb_score": 0.868,
        "gap": 0.026,
        "canary_auc": 0.504,
        "gb_noise": 0.801,
        "lr_noise": 0.771,
        "p_value": 0.184,
        "test_auc": 0.778,
        "rate_female": 74,
        "rate_male": 19,
        "rate_class1": 63,
        "rate_class3": 24,
        "champion_name": "Logistic Regression L2",
        "cells_count": 28
    }

    agents_and_rounds = [
        (framer, "problem_statement"),
        (framer, "metric_selection"),
        (wrangler, "data_understanding"),
        (wrangler, "data_cleaning"),
        (wrangler, "feature_engineering"),
        (guardian, "split_data"),
        (guardian, "baseline_candidates"),
        (guardian, "overfit_check"),
        (guardian, "canary_noise"),
        (guardian, "significance_test"),
        (guardian, "final_eval"),
        (storyteller, "key_findings"),
        (storyteller, "data_storytelling"),
        (storyteller, "recommendations"),
        (notebook, "build_notebook"),
    ]

    for agent, r_key in agents_and_rounds:
        t, m, d = agent.generate_offline_dialogue(r_key, test_facts)
        assert len(t) <= 28, f"Title {t} terlalu panjang untuk {r_key}"
        assert len(d) <= 190, f"Dialog {d} terlalu panjang untuk {r_key}"
        assert m in ("calm", "angry", "shock", "happy")


def test_demo_titanic_debate_json_validity():
    demo_path = Path("data/demo_titanic.debate.json")
    assert demo_path.exists(), "demo_titanic.debate.json belum dibuat"

    with open(demo_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Validasi skema Pydantic
    doc = DebateDocument.model_validate(data)
    assert doc.meta.dataset_name == "titanic.csv"
    assert len(doc.rounds) >= 14
    assert len(doc.leaderboard) >= 4
    assert len(doc.qa) >= 5

    # Validasi setiap babak
    for r in doc.rounds:
        assert len(r.title) <= 28
        assert len(r.dialog) <= 190
        assert len(r.evidence) <= 85
        assert r.chart.type in ("bar", "line", "roc", "confusion", "heatmap", "hist", "scatter")
