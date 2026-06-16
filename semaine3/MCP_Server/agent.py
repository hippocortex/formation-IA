import asyncio
import json
from mcp.client import Client

class Agent:
    def __init__(self):
        self.client = Client(command="python", args=["mcp_server_with_prompt_templates.py"])

    async def handle_query(self, user_query: str):
        await self.client.connect()

        # 1. Récupérer les templates
        templates = await self.client.call_tool("list_prompt_templates", {})

        # 2. Choisir le template le plus pertinent
        template_name = self._select_template(user_query, templates)
        if not template_name:
            return "Désolé, je ne sais pas comment répondre à cette requête."

        # 3. Récupérer et remplir le template
        template = await self.client.call_tool("get_prompt_template", {"template_name": template_name})
        filled_prompt = self._fill_template(template, user_query)

        # 4. Envoyer au LLM (simulé ici)
        llm_response = self._ask_llm(filled_prompt)

        # 5. Exécuter l'action
        action = json.loads(llm_response)
        if action["action"] != "none":
            result = await self.client.call_tool(action["action"], action["args"])
            return f"Résultat : {result}"
        else:
            return action["response"]

    def _select_template(self, user_query: str, templates: list) -> Optional[str]:
        """Sélectionne le template le plus pertinent."""
        user_query = user_query.lower()
        for template in templates:
            if "calcul" in user_query and template["name"] == "calculate_prompt":
                return "calculate_prompt"
            elif ("fichier" in user_query or "pdf" in user_query) and template["name"] == "read_file_prompt":
                return "read_file_prompt"
            elif "résumé" in user_query and template["name"] == "summarize_pdf_prompt":
                return "summarize_pdf_prompt"
        return None

    def _fill_template(self, template: dict, user_query: str) -> str:
        """Remplit les placeholders du template."""
        placeholders = template["placeholders"]
        filled = template["template"]
        for placeholder in placeholders:
            # Extraire la valeur depuis user_query (simplifié)
            if placeholder == "expression":
                # Exemple : "Calcule 2 + 2" → expression = "2 + 2"
                filled = filled.replace(f"{{{placeholder}}}", user_query.split("calcule")[1].strip())
            elif placeholder == "filename":
                # Exemple : "Lis maths.pdf" → filename = "maths.pdf"
                filled = filled.replace(f"{{{placeholder}}}", user_query.split("fichier")[1].strip())
        return filled

    def _ask_llm(self, prompt: str) -> str:
        """Simule un appel à un LLM."""
        # En pratique, utilise une API LLM réelle
        if "calculate" in prompt.lower():
            import re
            match = re.search(r"calculer l'expression suivante : ([^\.]+)", prompt)
            if match:
                expression = match.group(1).strip()
                return f'{{"action": "calculate", "args": {{"expression": "{expression}"}}}}'
        elif "lire le fichier" in prompt.lower():
            match = re.search(r"lire le fichier suivant : ([^\.]+)", prompt)
            if match:
                filename = match.group(1).strip()
                return f'{{"action": "read_file", "args": {{"filename": "{filename}"}}}}'
        return '{"action": "none", "response": "Je ne peux pas répondre."}'

# Exemple d'utilisation
async def main():
    agent = Agent()
    print(await agent.handle_query("Calcule 2 + 2"))
    print(await agent.handle_query("Lis le fichier maths.pdf"))

if __name__ == "__main__":
    asyncio.run(main())