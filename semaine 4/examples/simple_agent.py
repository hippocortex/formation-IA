# examples/simple_agent.py
import os
from mini_framework import AgentConfig, ToolRegistry, Agent

# Vérification préalable de la clé API
if "OPENAI_API_KEY" not in os.environ:
    print("ATTENTION : La variable d'environnement OPENAI_API_KEY est manquante.")

# 1. Création de notre registre et déclaration d'outils
registry = ToolRegistry()

@registry.register
def additionner_nombres(a: int, b: int) -> dict:
    """
    Additionne deux nombres entiers.
    
    Args:
        a: Le premier nombre entier.
        b: Le second nombre entier.
    """
    return {"resultat": a + b}

# 2. Configuration et instanciation de l'agent
config = AgentConfig(temperature=0.0, max_turns=5)
agent = Agent(config=config, registry=registry)

# 3. Lancement d'une requête nécessitant l'appel d'outil
print("Démarrage de la boucle ReAct de l'agent...")
resultat_conv = agent.run(
    user_prompt="Peux-tu additionner 432 et 568 s'il te plaît?",
    system_prompt="Tu es un agent mathématique rigoureux. Utilise obligatoirement tes outils pour calculer."
)

# 4. Affichage du déroulement pas-à-pas de l'exécution
print("\n--- Historique d'exécution de la conversation ---")
for msg in resultat_conv.messages:
    text = f"[{msg.role.upper()}] "
    if msg.content:
        text += f"Contenu : {msg.content}"
    if msg.tool_calls:
        text += f" (Demande d'outils: {[tc['function']['name'] for tc in msg.tool_calls]})"
    print(text)