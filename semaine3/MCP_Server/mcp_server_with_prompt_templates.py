import os
import asyncio
from mcp.server import Server
from mcp.types import Tool, EmbeddedResource
from typing import List, Optional, Dict

PDF_DIR = "./pdfs"
app = Server("prompt-templates-server")

# --- Templates de prompts ---
# Chaque template est un dictionnaire avec :
# - name: Nom du template
# - description: Description pour le LLM/agent
# - template: Le template de prompt (avec des placeholders comme {expression}, {filename}, etc.)
PROMPT_TEMPLATES = {
    "calculate": {
        "name": "calculate_prompt",
        "description": "Template pour demander un calcul mathématique. Utilise l'outil `calculate`.",
        "template": """
        L'utilisateur demande de calculer l'expression suivante : {expression}.
        Utilise l'outil `calculate(expression: str)` pour obtenir le résultat.
        Retourne uniquement le résultat du calcul.
        """,
    },
    "read_file": {
        "name": "read_file_prompt",
        "description": "Template pour demander la lecture d'un fichier. Utilise l'outil `read_file`.",
        "template": """
        L'utilisateur demande de lire le fichier suivant : {filename}.
        Utilise l'outil `read_file(filename: str)` pour obtenir le contenu du fichier.
        Si le fichier n'existe pas, retourne une erreur claire.
        """,
    },
    "summarize_pdf": {
        "name": "summarize_pdf_prompt",
        "description": "Template pour résumer un PDF. Utilise `read_file` puis un LLM pour générer un résumé.",
        "template": """
        L'utilisateur demande un résumé du fichier PDF : {filename}.
        1. Utilise `read_file(filename: str)` pour lire le contenu du PDF.
        2. Génère un résumé de 3 phrases maximum en français.
        """,
    },
}

# --- Outils ---
@app.tool(
    description="Lit le contenu d'un fichier dans le dossier `pdfs/`. Exemple : `read_file('mon_fichier.pdf')`.",
)
async def read_file(filename: str) -> Optional[bytes]:
    path = os.path.join(PDF_DIR, filename)
    if os.path.exists(path):
        with open(path, "rb") as f:
            return f.read()
    return None

@app.tool(
    description="Évalue une expression mathématique. Exemple : `calculate('2 + 3 * 4')`.",
)
async def calculate(expression: str) -> str:
    try:
        result = eval(expression, {"__builtins__": None}, {})
        return str(result)
    except:
        return "Erreur : expression invalide."

# --- Outil pour lister les templates de prompts ---
@app.tool(
    description="Liste les templates de prompts disponibles pour guider le LLM.",
)
async def list_prompt_templates() -> List[Dict]:
    """Retourne la liste des templates de prompts disponibles."""
    return [
        {
            "name": template["name"],
            "description": template["description"],
            "placeholders": list(
                {m.group(1) for m in __import__("re").finditer(r"\{(\w+)\}", template["template"])}
            ),
        }
        for template in PROMPT_TEMPLATES.values()
    ]

# --- Outil pour récupérer un template de prompt ---
@app.tool(
    description="Récupère un template de prompt par son nom. Exemple : `get_prompt_template('calculate_prompt')`.",
)
async def get_prompt_template(template_name: str) -> Optional[Dict]:
    """Retourne le template de prompt demandé."""
    template = PROMPT_TEMPLATES.get(template_name)
    if template:
        return {
            "name": template["name"],
            "description": template["description"],
            "template": template["template"],
            "placeholders": list(
                {m.group(1) for m in __import__("re").finditer(r"\{(\w+)\}", template["template"])}
            ),
        }
    return None

if __name__ == "__main__":
    asyncio.run(app.run_stdio())