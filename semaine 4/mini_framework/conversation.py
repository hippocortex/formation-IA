# mini_framework/conversation.py
from typing import List, Dict, Any
from mini_framework.message import Message

class Conversation:
    """Conteneur d'état linéaire gérant l'historique de discussion à court terme."""
    def __init__(self):
        self.messages: List[Message] =

    def add_message(self, message: Message) -> None:
        """Ajoute un message validé à la conversation."""
        self.messages.append(message)

    def get_api_payload(self) -> List]:
        """Génère la liste sérialisée de messages requis pour l'API du modèle."""
        return [msg.to_openai_dict() for msg in self.messages]

    def clear(self) -> None:
        """Réinitialise la mémoire conversationnelle immédiate."""
        self.messages =