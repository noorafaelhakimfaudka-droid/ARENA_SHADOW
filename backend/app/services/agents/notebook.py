from typing import Any, Dict, Tuple
from backend.app.services.agents.base import BaseAgent


class NotebookAgent(BaseAgent):
    def __init__(self):
        super().__init__(
            name="NOTEBOOK BUILDER",
            role="Pembuat kode notebook .ipynb",
            color="#5B9BB5",
            chip="nb.build()",
            tail=("r", 84)
        )

    def generate_offline_dialogue(
        self, round_key: str, facts: Dict[str, Any]
    ) -> Tuple[str, str, str]:
        nb_file = facts.get("notebook_filename", "shadow_arena.ipynb")
        cells = facts.get("cells_count", 28)
        dialog = (
            f"Semua temuan kita kurakit jadi notebook {nb_file} berurutan: "
            f"EDA, split, pipeline, evaluasi, hingga model final. "
            f"Sekitar {cells} sel siap dijalankan langsung di Jupyter!"
        )
        return "Rakit Notebook", "happy", dialog[:190]
