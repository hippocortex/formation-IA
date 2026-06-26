# mini_framework/tools.py
import inspect
import functools
import re
from typing import Callable, Any, Dict, get_type_hints, Tuple

# Table d'équivalence entre types Python et JSON Schema
MAP_TYPES_JSON = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
    list: "array",
    dict: "object",
    type(None): "null"
}

class Tool:
    """Encapsule une fonction exécutable et génère dynamiquement sa spécification JSON."""
    def __init__(self, func: Callable[..., Any]):
        self.func = func
        self.name = func.__name__
        self.docstring = inspect.getdoc(func) or ""
        self.schema = self._generer_schema()

    def __call__(self, *args, **kwargs) -> Any:
        return self.func(*args, **kwargs)

    def _parse_docstring(self) -> Tuple]:
        """Extrait la description globale et les descriptions de paramètres au format Google."""
        if not self.docstring:
            return "Aucune description fournie.", {}
            
        lines = [line.strip() for line in self.docstring.split("\n")]
        description_lines =
        param_descriptions = {}
        in_args = False

        for line in lines:
            if re.match(r"^(Args|Arguments|Parameters):\s*$", line, re.IGNORECASE):
                in_args = True
                continue
            if in_args:
                if re.match(r"^(Returns|Raises|Yields):\s*$", line, re.IGNORECASE):
                    break
                if ":" in line:
                    parts = line.split(":", 1)
                    param_name = parts.strip()
                    param_desc = parts.[1]strip()
                    param_descriptions[param_name] = param_desc
            else:
                description_lines.append(line)

        return "\n".join(description_lines).strip(), param_descriptions

    def _generer_schema(self) -> Dict[str, Any]:
        """Génère le schéma fonctionnel conforme aux API de Function Calling d'OpenAI."""
        signature = inspect.signature(self.func)
        type_hints = get_type_hints(self.func)
        desc_generale, descs_params = self._parse_docstring()
        
        properties = {}
        required =

        for nom_param, param in signature.parameters.items():
            if nom_param in ["self", "cls", "context"]:
                continue

            type_python = type_hints.get(nom_param, param.annotation)
            type_json = MAP_TYPES_JSON.get(type_python, "string")
            param_desc = descs_params.get(nom_param, f"Paramètre d'entrée : {nom_param}")

            properties[nom_param] = {
                "type": type_json,
                "description": param_desc
            }
            if param.default is inspect.Parameter.empty:
                required.append(nom_param)

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": desc_generale,
                "parameters": {
                    "type": "object",
                    "properties": properties,
                    "required": required
                }
            }
        }

def tool(func: Callable[..., Any]) -> Tool:
    """Décorateur pour transformer une fonction Python standard en objet Tool."""
    if isinstance(func, Tool):
        return func
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return Tool(wrapper)