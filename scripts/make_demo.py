import json
import sys
from pathlib import Path

# Add project root to path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT_DIR))

from backend.app.services.dataset import load_csv_safely
from backend.app.services.problem import infer_problem
from backend.app.services.modeling import run_full_modeling_pipeline
from backend.app.services.insights import generate_insights
from backend.app.services.orchestrator import build_debate_document


def main():
    print("=" * 60)
    print("SHADOW ARENA: Menjalankan Pipeline Nyata Titanic -> Demo Debate")
    print("=" * 60)

    titanic_csv = ROOT_DIR / "data" / "titanic.csv"
    if not titanic_csv.exists():
        print(f"Error: {titanic_csv} tidak ditemukan.")
        sys.exit(1)

    print("1. Membaca dataset Titanic...")
    df, name = load_csv_safely(titanic_csv)
    print(f"   Dimuat: {len(df)} baris, {len(df.columns)} kolom.")

    print("2. Inferensi Problem Statement...")
    prob = infer_problem(df, requested_target="survived")
    print(f"   Target: {prob.target}, Task: {prob.task}, Metric: {prob.metric}")

    print("3. Menjalankan Full ML Pipeline...")
    ml_results = run_full_modeling_pipeline(df, prob)
    print(f"   Champion: {ml_results['champion_name']}")
    print(f"   Test AUC: {ml_results['final_eval']['test_auc']}")

    print("4. Mengekstrak Insight & Segmentasi...")
    insights = generate_insights(df, prob.target, ml_results)

    print("5. Merakit Debat Multi-Agent...")
    notebook_info = {
        "filename": "shadow_arena.ipynb",
        "valid": True,
        "cells_count": 28
    }

    doc = build_debate_document(
        session_id="demo_titanic",
        dataset_name="titanic.csv",
        df=df,
        problem=prob,
        ml_results=ml_results,
        insights_data=insights,
        notebook_info=notebook_info
    )

    out_file = ROOT_DIR / "data" / "demo_titanic.debate.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(doc.model_dump(), f, indent=2, ensure_ascii=False)

    print(f"6. Sukses! File disimpan ke: {out_file}")
    print(f"   Total Babak: {len(doc.rounds)}")
    print(f"   Mode: {doc.meta.mode}")
    print("=" * 60)


if __name__ == "__main__":
    main()
