# mini_framework/config.py
"""
Gestion de la configuration de l'infrastructure de l'agent
avec validation automatique d'environnement.
"""

import os
from dataclasses import dataclass
from mini_framework.exceptions import ConfigurationError

@dataclass
class AgentConfig:
    """Conserve et valide les hyperparamètres logiques de notre moteur d'exécution."""
    model: str = "gpt-4o-mini"
    temperature: float = 0.0
    max_turns: int = 10
    api_key: str = ""

    def __post_init__(self) -> None:
        # Si aucune clé n'est fournie, recherche automatique dans les variables d'environnement
        if not self.api_key:
            self.api_key = os.environ.get("OPENAI_API_KEY", "")

        # Validation stricte en production : empêche l'instanciation si la clé d'API est absente
        if not self.api_key:
            raise ConfigurationError(
                "La clé d'API OpenAI est introuvable. Veuillez configurer la variable d'environnement "
                "OPENAI_API_KEY ou passer explicitement le paramètre 'api_key' à la configuration."
            )