from typing import Any, Dict, Tuple
from backend.app.services.agents.base import BaseAgent


class InsightStoryteller(BaseAgent):
    def __init__(self):
        super().__init__(
            name="INSIGHT STORYTELLER",
            role="Insight, visualisasi & data storytelling",
            color="#D9703F",
            chip="plot.story()",
            tail=("l", 84)
        )

    def generate_offline_dialogue(
        self, round_key: str, facts: Dict[str, Any]
    ) -> Tuple[str, str, str]:
        if round_key == "key_findings":
            f_rate = facts.get("rate_female", 74)
            m_rate = facts.get("rate_male", 19)
            c1_rate = facts.get("rate_class1", 63)
            c3_rate = facts.get("rate_class3", 24)
            dialog = (
                f"Lihat ini! Perempuan selamat {f_rate}%, laki-laki cuma {m_rate}%. "
                f"Kelas 1 selamat {c1_rate}%, kelas 3 hanya {c3_rate}%. Data ini menyimpan pola nyata."
            )
            return "Temuan Utama", "shock", dialog[:190]

        elif round_key == "data_storytelling":
            f1 = facts.get("top_feature_1", "sex")
            f2 = facts.get("top_feature_2", "pclass")
            dialog = (
                f"Ceritanya begini: 'perempuan dan anak dulu' bukan sekadar mitos, "
                f"kelas sosial juga menentukan evakuasi. Fitur {f1} dan {f2} paling dominan."
            )
            return "Data Storytelling", "happy", dialog[:190]

        elif round_key == "recommendations":
            m_name = facts.get("champion_name", "Logistic Regression L2")
            dialog = (
                f"Pesan untuk pemangku kepentingan: model {m_name} siap dipakai karena transparan, "
                f"mudah dijelaskan lewat koefisien, dan stabil terhadap derau."
            )
            return "Rekomendasi", "calm", dialog[:190]

        return "Cerita Data", "calm", "Data menyampaikan wawasan berharga bagi keputusan kita."
