# mini_framework/memory.py
from typing import Dict, List
from mini_framework.message import Message

class Memory:
    """Simule un moteur de persistance pour sauvegarder et restaurer des sessions."""
    def __init__(self):
        self._db: Dict[str, List[Message]] = {}

    def save_session(self, session_id: str, messages: List[Message]) -> None:
        """Sauvegarde l'historique complet d'une conversation."""
        self._db[session_id] = list(messages)

    def load_session(self, session_id: str) -> List[Message]:
        """Charge l'historique complet d'une session ou retourne une liste vide."""
        return self._db.get(session_id,)

    def clear_session(self, session_id: str) -> None:
        """Supprime une session sauvegardée."""
        if session_id in self._db:
            del self._db[session_id]