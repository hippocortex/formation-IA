# mini_framework/registry.py
import json
from typing import Dict, List, Any, Callable
from mini_framework.tools import Tool, tool

class ToolRegistry:
    """Registre centralisé pour la découverte et l'exécution sécurisée d'outils."""
    def __init__(self):
        self._tools: Dict = {}

    def register(self, item: Any) -> Callable[..., Any]:
        """Enregistre un outil au sein du registre."""
        if isinstance(item, Tool):
            self._tools[item.name] = item
            return item.func
        elif callable(item):
            wrapped = tool(item)
            self._tools[wrapped.name] = wrapped
            return item
        raise TypeError("L'élément enregistré doit être exécutable ou une instance de Tool.")

    def get_schemas(self) -> List]:
        """Retourne la liste des schémas d'outils au format attendu par OpenAI."""
        return [t.schema for t in self._tools.values()]

    def execute(self, name: str, args_json: str) -> str:
        """Exécute un outil par son nom avec des arguments au format JSON brut."""
        if name not in self._tools:
            return json.dumps({"error": f"L'outil '{name}' est introuvable au registre."}, ensure_ascii=False)
        try:
            # Conversion sécurisée des arguments
            args = json.loads(args_json) if isinstance(args_json, str) else args_json
            result = self._tools[name](**args)
            return json.dumps(result, ensure_ascii=False)
        except Exception as e:
            return json.dumps({"error": f"Échec d'exécution de '{name}' : {str(e)}"}, ensure_ascii=False)