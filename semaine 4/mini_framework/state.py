# mini_framework/state.py
from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class AgentState:
    """
    Représente l'état de données partagé et immuable au sein d'un graphe d'états.
    """
    task: str                         # La consigne d'origine de l'utilisateur
    draft: str = ""                   # Le brouillon d'article actuel
    feedback: str = ""                # Les commentaires du relecteur
    revision_count: int = 0           # Le nombre de cycles effectués
    approved: bool = False            # Le statut d'approbation final
    metadata: Dict[str, Any] = field(default_factory=dict)