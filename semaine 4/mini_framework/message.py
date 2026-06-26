# mini_framework/message.py
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

@dataclass
class Message:
    """Représentation universelle d'un message unitaire au sein du framework."""
    role: str
    content: Optional[str] = None
    name: Optional[str] = None
    tool_call_id: Optional[str] = None
    tool_calls: Optional]] = None

    def to_openai_dict(self) -> Dict[str, Any]:
        """Convertit l'instance de message interne en dictionnaire compatible avec l'API OpenAI."""
        payload = {"role": self.role}
        if self.content is not None:
            payload["content"] = self.content
        if self.name is not None:
            payload["name"] = self.name
        if self.tool_call_id is not None:
            payload["tool_call_id"] = self.tool_call_id
        if self.tool_calls is not None:
            payload["tool_calls"] = self.tool_calls
        return payload