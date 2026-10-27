from typing import Any, Dict, Tuple
from backend.app.services.agents.base import BaseAgent


class ProblemFramer(BaseAgent):
    def __init__(self):
        super().__init__(
            name="PROBLEM FRAMER",
            role="Perumus problem statement",
            color="#E3A72F",
            chip="problem.frame()",
            tail=("t", 510)
        )

    def generate_offline_dialogue(
        self, round_key: str, facts: Dict[str, Any]
    ) -> Tuple[str, str, str]:
        target = facts.get("target", "target")
        task = facts.get("task", "klasifikasi biner")
        metric = facts.get("metric", "ROC-AUC")

        if round_key == "problem_statement":
            ds_name = facts.get("dataset_name", "dataset")
            dialog = (
                f"Tunggu, jangan ngoding dulu! Dataset ini mau menjawab apa? "
                f"Kita memprediksi {target}. Task = {task}. "
                f"Itu problem statement kita."
            )
            return "Problem Statement", "calm", dialog[:190]

        elif round_key == "metric_selection":
            c0 = facts.get("class_0_pct", 50)
            c1 = facts.get("class_1_pct", 50)
            dialog = (
                f"Kelas tidak seimbang ({c1}% vs {c0}%), jadi akurasi bisa menipu! "
                f"Gunakan {metric} dan PR-AUC untuk evaluasi objektif tanpa ilusi."
            )
            return "Pilih Metrik", "angry", dialog[:190]

        return "Diskusi Masalah", "calm", f"Fokus utama kita adalah memprediksi {target}."
