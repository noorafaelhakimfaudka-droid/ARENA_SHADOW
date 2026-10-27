from abc import ABC, abstractmethod
from typing import Any, Dict, Tuple


class BaseAgent(ABC):
    def __init__(self, name: str, role: str, color: str, chip: str, tail: Tuple[str, int]):
        self.name = name
        self.role = role
        self.color = color
        self.chip = chip
        self.tail = tail  # e.g. ("l", 36), ("t", 510), ("r", 36)

    @abstractmethod
    def generate_offline_dialogue(
        self, round_key: str, facts: Dict[str, Any]
    ) -> Tuple[str, str, str]:
        """
        Menghasilkan tuple (title, mood, dialog) deterministik berdasarkan fakta nyata.
        Title <= 28 karakter, dialog <= 190 karakter.
        """
        pass
