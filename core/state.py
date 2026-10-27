# ml-agents/core/state.py
"""
Manajemen Shared State Terpadu (state.json).
- Objek state bersama yang diteruskan secara sekuensial antar agen.
- Menyimpan fakta komputasi Python, keputusan JSON para agen, transkrip debat, dan metrik akhir.
- Dapat diserialisasi dan dibaca kembali kapan saja.
"""

from __future__ import annotations
import datetime
import json
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class SharedState:
    run_id: str
    csv_path: str
    created_at: str = field(default_factory=lambda: datetime.datetime.now().isoformat())
    
    # 1. Info Dataset Awal (Dari Profiling Python)
    dataset_info: Dict[str, Any] = field(default_factory=dict)
    
    # 2. Hasil Framing (Agen 1 / Framing Debate)
    framing: Dict[str, Any] = field(default_factory=dict)
    
    # 3. Rencana & Eksekusi Data Cleaning (Agen 2 / Data Agent)
    data_plan: Dict[str, Any] = field(default_factory=dict)
    data_execution: Dict[str, Any] = field(default_factory=dict)
    
    # 4. Modeling, CV, Cek Kualitas & Evaluasi (Agen 3 / Modeling Agent)
    modeling_plan: Dict[str, Any] = field(default_factory=dict)
    modeling_results: Dict[str, Any] = field(default_factory=dict)
    
    # 5. Visualisasi, Storytelling & Insight (Agen 4 / Insight Agent)
    insights: Dict[str, Any] = field(default_factory=dict)
    figures: List[str] = field(default_factory=list)
    
    # 6. Notebook Deliverable (Agen 5 / Notebook Generator)
    notebook_info: Dict[str, Any] = field(default_factory=dict)
    
    # 7. Transkrip Debat Nyata Antar 6 Agen AI (Live Dynamic Debate Log)
    debate_transcripts: List[Dict[str, Any]] = field(default_factory=list)
    
    # 8. Ekspor Artefak Prediksi (M5)
    model_path: str = ""
    schema_path: str = ""

    def add_debate_turn(
        self,
        round_name: str,
        agent_name: str,
        role: str,
        color: str,
        stance: str,
        argument: str,
        evidence: Dict[str, Any] | List[Any] | str = "",
        decision: Optional[Dict[str, Any]] = None
    ) -> None:
        """Menambahkan satu giliran bicara/argumen agen ke dalam transkrip debat nyata."""
        turn = {
            "round": round_name,
            "agent": agent_name,
            "role": role,
            "color": color,
            "stance": stance,
            "argument": argument,
            "evidence": evidence,
            "decision": decision or {},
            "timestamp": datetime.datetime.now().isoformat()
        }
        self.debate_transcripts.append(turn)

    def save_to_file(self, output_dir: Path | str) -> Path:
        """Menyimpan seluruh state ke state.json di direktori run yang ditentukan."""
        out_path = Path(output_dir) / "state.json"
        out_path.parent.mkdir(parents=True, exist_ok=True)
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(asdict(self), f, indent=2, ensure_ascii=False)
        return out_path

    @classmethod
    def load_from_file(cls, state_path: Path | str) -> SharedState:
        """Membaca kembali state dari state.json."""
        with open(state_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return cls(**data)
