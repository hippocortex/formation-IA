import asyncio
import json
from mcp.client import Client

# Simulation d'un appel à un LLM
def ask_llm(prompt: str) -> str:
    """
    Simule un appel à un LLM avec un prompt complet.
    En pratique, utilise une API LLM (Mistral, OpenAI, etc.).
    """
    # Logique simplifiée pour l'exemple
    if "calculate" in prompt.lower():
        # Extraire l'expression (ex: {expression} = "2 + 2")
        import re
        match = re.search(r"\{expression\}:?\s*([^\}]+)", prompt)
        if match:
            expression = match.group(1).strip()
            return f'{{"action": "calculate", "args": {{"expression": "{expression}"}}}}'
    elif "read_file" in prompt.lower():
        match = re.search(r"\{filename\}:?\s*([^\}]+)", prompt)
        if match:
            filename = match.group(1).strip()
            return f'{{"action": "read_file", "args": {{"filename": "{filename}"}}}}'
    elif "summarize_pdf" in prompt.lower():
        match = re.search(r"\{filename\}:?\s*([^\}]+)", prompt)
        if match:
            filename = match.group(1).strip()
            return f'{{"action": "read_file", "args": {{"filename": "{filename}"}}}}'
    return '{"action": "none", "response": "Je ne peux pas répondre."}'

async def main():
    client = Client(command="python", args=["mcp_server_with_prompt_templates.py"])
    await client.connect()

    # --- 1. Récupérer les templates de prompts ---
    templates = await client.call_tool("list_prompt_templates", {})
    print("Templates de prompts disponibles :")
    for template in templates:
        print(f"- {template['name']} : {template['description']}")
        print(f"  Placeholders : {template['placeholders']}")

    # --- 2. Exemple : Utiliser le template "calculate_prompt" ---
    print("\n--- Utilisation du template 'calculate_prompt' ---")
    template_name = "calculate_prompt"
    template = await client.call_tool("get_prompt_template", {"template_name": template_name})
    print(f"Template : {template['template']}")

    # Remplir le placeholder {expression}
    user_expression = "2 + 3 * 4"
    filled_prompt = template["template"].format(expression=user_expression)
    print(f"Prompt rempli : {filled_prompt}")

    # Envoyer au LLM
    llm_response = ask_llm(filled_prompt)
    print(f"Réponse du LLM : {llm_response}")

    # Exécuter l'action
    action = json.loads(llm_response)
    if action["action"] != "none":
        result = await client.call_tool(action["action"], action["args"])
        print(f"Résultat de {action['action']} : {result}")

    # --- 3. Exemple : Utiliser le template "read_file_prompt" ---
    print("\n--- Utilisation du template 'read_file_prompt' ---")
    template_name = "read_file_prompt"
    template = await client.call_tool("get_prompt_template", {"template_name": template_name})
    user_filename = "maths.pdf"
    filled_prompt = template["template"].format(filename=user_filename)
    print(f"Prompt rempli : {filled_prompt}")

    llm_response = ask_llm(filled_prompt)
    print(f"Réponse du LLM : {llm_response}")

    action = json.loads(llm_response)
    if action["action"] != "none":
        result = await client.call_tool(action["action"], action["args"])
        print(f"Contenu du fichier (premiers 50 octets) : {result[:50]}")

    await client.close()

if __name__ == "__main__":
    asyncio.run(main())