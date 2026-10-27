from typing import Any, Dict, Tuple
from backend.app.services.agents.base import BaseAgent


class DataWrangler(BaseAgent):
    def __init__(self):
        super().__init__(
            name="DATA WRANGLER",
            role="Data understanding, cleaning & feature engineering",
            color="#8DB255",
            chip="df.clean()",
            tail=("l", 36)
        )

    def generate_offline_dialogue(
        self, round_key: str, facts: Dict[str, Any]
    ) -> Tuple[str, str, str]:
        n_rows = facts.get("n_rows", 891)
        n_cols = facts.get("n_cols", 12)

        if round_key == "data_understanding":
            missing_info = facts.get("missing_summary", "beberapa nilai kosong")
            dialog = (
                f"Kuperiksa dulu isi perutnya: {n_rows} baris, {n_cols} kolom. "
                f"{missing_info}. Kita petakan tipenya sebelum melangkah!"
            )
            return "Data Understanding", "shock", dialog[:190]

        elif round_key == "data_cleaning":
            clean_act = facts.get("clean_action", "duplikat dibuang")
            dialog = (
                f"Kubersihkan secukupnya: {clean_act}. "
                f"Imputasi dan scaling kusimpan rapi di pipeline agar tidak ada kebocoran!"
            )
            return "Data Cleaning", "happy", dialog[:190]

        elif round_key == "feature_engineering":
            feats = facts.get("engineered_features", "fitur baru")
            vif_max = facts.get("vif_max", 2.6)
            dialog = (
                f"Boleh aku meracik? Fitur {feats}. "
                f"Sinyal baru yang masuk akal dan kuperiksa VIF max={vif_max} aman dari multikolinearitas."
            )
            return "Feature Engineering", "happy", dialog[:190]

        return "Eksplorasi Data", "calm", f"Data diproses: {n_rows} baris siap diolah."
