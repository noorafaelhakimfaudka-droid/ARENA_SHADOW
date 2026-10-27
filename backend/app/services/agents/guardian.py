from typing import Any, Dict, Tuple
from backend.app.services.agents.base import BaseAgent


class ModelGuardian(BaseAgent):
    def __init__(self):
        super().__init__(
            name="MODEL GUARDIAN",
            role="Pemilih model, penjaga leakage & overfit",
            color="#B83A2E",
            chip="model.fit()",
            tail=("r", 36)
        )

    def generate_offline_dialogue(
        self, round_key: str, facts: Dict[str, Any]
    ) -> Tuple[str, str, str]:
        if round_key == "split_data":
            n_train = facts.get("n_train", 712)
            n_test = facts.get("n_test", 179)
            dialog = (
                f"STOP! Belum ada yang boleh menghitung statistik sebelum split! "
                f"Train 80% ({n_train}), test 20% ({n_test}) stratified dan test kugembok rapat."
            )
            return "Split Sebelum Apa Pun", "angry", dialog[:190]

        elif round_key == "leakage_audit":
            has_leak = facts.get("has_leak", False)
            if has_leak:
                leak_col = facts.get("leak_col", "kolom")
                corr = facts.get("corr", 1.0)
                dialog = (
                    f"Hmph, kutemukan penipu! Kolom '{leak_col}' memiliki korelasi {corr:.2f} > 0.85 dengan target. "
                    f"Model yang pakai itu cuma menyontek. Buang sekarang!"
                )
                return "Detektif Kebocoran", "angry", dialog[:190]
            else:
                dialog = (
                    f"Kusaring semua fitur: korelasi terhadap target aman di bawah 0.85 "
                    f"dan tidak ada ID-like column. Dataset bersih dari kebocoran!"
                )
                return "Detektif Kebocoran", "calm", dialog[:190]

        elif round_key == "baseline_candidates":
            dummy = facts.get("dummy_score", 0.500)
            logreg = facts.get("logreg_score", 0.782)
            rf = facts.get("rf_score", 0.851)
            gb = facts.get("gb_score", 0.868)
            dialog = (
                f"Kandidat masuk arena! Dummy cuma {dummy:.3f}. "
                f"Logistic {logreg:.3f}, Random Forest {rf:.3f}, Gradient Boosting {gb:.3f} di CV 5-lipatan."
            )
            return "Baseline & Kandidat", "happy", dialog[:190]

        elif round_key == "overfit_check":
            gap = facts.get("gap", 0.026)
            dialog = (
                f"Kurva belajar bicara jujur. Gap train-validasi cuma {gap:.3f}, "
                f"tidak overfit parah dan jauh di atas dummy. Model seimbang."
            )
            return "Cek Overfit & Underfit", "calm", dialog[:190]

        elif round_key == "canary_noise":
            c_auc = facts.get("canary_auc", 0.504)
            gb_drop = facts.get("gb_noise", 0.801)
            lr_drop = facts.get("lr_noise", 0.771)
            dialog = (
                f"Label diacak 100%: skor jatuh ke {c_auc:.3f}, bersih kebocoran! "
                f"Uji derau 15%: GB ke {gb_drop:.3f}, Logistic stabil di {lr_drop:.3f}."
            )
            return "Uji Kanari & Derau", "shock", dialog[:190]

        elif round_key == "significance_test":
            p = facts.get("p_value", 0.184)
            chosen = facts.get("champion_name", "Logistic Regression L2")
            dialog = (
                f"Uji t terkoreksi Nadeau-Bengio menghasilkan p = {p:.3f} > 0.05. "
                f"Selisih belum signifikan nyata, jadi pilih yang sederhana dan stabil: {chosen}."
            )
            return "Uji Signifikansi", "calm", dialog[:190]

        elif round_key == "final_eval":
            test_auc = facts.get("test_auc", 0.778)
            m_name = facts.get("champion_name", "Logistic Regression L2")
            dialog = (
                f"Gembok test kubuka, sekali saja. {m_name} mencapai AUC {test_auc:.3f} "
                f"di data uji baru. Tidak ada kebocoran, hasil konsisten!"
            )
            return "Evaluasi Akhir", "happy", dialog[:190]

        return "Pengawasan Model", "calm", "Kualitas model diverifikasi secara ketat."
