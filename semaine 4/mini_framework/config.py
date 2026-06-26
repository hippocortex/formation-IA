# mini_framework/config.py
import os
from dataclasses import dataclass

@dataclass
class AgentConfig:
    """Conserve les paramètres d'exécution et d'infrastructure de l'agent."""
    model: str = "gpt-4o-mini"
    temperature: float = 0.0
    max_turns: int = 10
    api_key: str = os.environ.get("OPENAI_API_KEY", "")