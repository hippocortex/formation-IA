# examples/writer_critic_openai_sdk.py
"""
Réimplémentation du workflow cyclique de correction rédactionnelle (Writer-Critic)
en utilisant l'OpenAI Agents SDK et le pattern d'orchestration par Handoffs.
"""

import asyncio
import os
from typing import Optional
from agents import Agent, Runner, handoff, RunContextWrapper, function_tool
from agents.run import RunConfig

# Vérification de sécurité pour la clé d'API
if "OPENAI_API_KEY" not in os.environ:
    print("ATTENTION : La variable d'environnement OPENAI_API_KEY est manquante.")

# ==========================================
# 1. Définition du Contexte Partagé Mutable
# ==========================================

class ProjectContext:
    """
    Conteneur d'état partagé entre nos agents.
    Il est passé de manière sécurisée sous forme de variable générique.
    """
    def __init__(self, task: str):
        self.task = task
        self.draft = ""
        self.feedback = ""
        self.revision_count = 0
        self.approved = False

# ==========================================
# 2. Déclaration des Outils Locaux (Tools)
# ==========================================

@function_tool
def update_article_draft(ctx: RunContextWrapper[ProjectContext], content: str) -> str:
    """
    Permet au rédacteur d'écrire ou de mettre à jour le brouillon d'un article.

    Args:
        content: Le texte complet rédigé pour le brouillon.
    """
    # Accès direct à l'état partagé typé via le wrapper de contexte
    ctx.context.draft = content
    ctx.context.revision_count += 1
    return f"Brouillon mis à jour avec succès (Révision {ctx.context.revision_count})."


@function_tool
def record_critic_feedback(ctx: RunContextWrapper[ProjectContext], comments: str, approve: bool) -> str:
    """
    Permet au relecteur d'enregistrer ses remarques ou de valider le brouillon.

    Args:
        comments: Les remarques détaillées sur les points d'amélioration de l'article.
        approve: Passer à True si l'article est parfait, False s'il doit être corrigé.
    """
    ctx.context.feedback = comments
    ctx.context.approved = approve
    return "Remarques enregistrées."

# ==========================================
# 3. Configuration et Instanciation des Agents
# ==========================================

# Instanciation de l'agent Rédacteur (Writer)
writer_agent = Agent[ProjectContext](
    name="Writer",
    model="gpt-4o-mini",
    instructions=(
        "Tu es un rédacteur professionnel d'articles de blog technique.\n"
        "1. Reçois le sujet demandé et rédige un brouillon initial.\n"
        "2. Utilise obligatoirement l'outil 'update_article_draft' pour enregistrer ton texte.\n"
        "3. Dès que ton brouillon est enregistré ou corrigé, tu DOIS passer la main au Critic "
        "en utilisant l'outil de transfert disponible (transfer_to_critic).\n"
        "N'invente rien d'autre et ne réponds pas directement à l'utilisateur."
    ),
    tools=[update_article_draft]
)

# Instanciation de l'agent Relecteur (Critic)
critic_agent = Agent[ProjectContext](
    name="Critic",
    model="gpt-4o-mini",
    instructions=(
        "Tu es un relecteur exigeant chargé d'analyser et valider les articles produits.\n"
        "1. Lis le brouillon actuel de l'article.\n"
        "2. Si l'article en est à sa 3ème révision ou plus, tu es satisfait : "
        "utilise 'record_critic_feedback' avec 'approve=True' et formule ta réponse finale de validation.\n"
        "3. Si l'article a moins de 3 révisions, tu DOIS exiger des améliorations : "
        "utilise 'record_critic_feedback' avec 'approve=False', décris les manques, "
        "puis transfère le contrôle au Writer en appelant 'transfer_to_writer'."
    ),
    tools=[record_critic_feedback]
)

# ==========================================
# 4. Résolution de la dépendance circulaire des Handoffs
# ==========================================

# Le Writer propose un transfert direct vers le Critic
writer_agent.handoffs = [critic_agent]

# Le Critic propose un transfert direct vers le Writer
critic_agent.handoffs = [writer_agent]

# ==========================================
# 5. Point d'Entrée d'Exécution Asynchrone
# ==========================================

async def main():
    print("--- Démarrage du Workflow cyclique via l'OpenAI Agents SDK ---")
    
    # 1. Initialisation de notre contexte d'exécution
    contexte_partage = ProjectContext(task="Les fondations de l'OpenAI Agents SDK en 2026")
    
    # 2. Requête d'entrée utilisateur
    user_prompt = f"Rédige un article complet sur : {contexte_partage.task}"

    # 3. Invocation de l'orchestrateur (Runner)
    # Le Runner gère en interne la boucle d'évaluation et intercepte les handoffs
    resultat = await Runner.run(
        starting_agent=writer_agent,
        input=user_prompt,
        context=contexte_partage,
        run_config=RunConfig(nest_handoff_history=True) # Compression automatique de l'historique de handoffs
    )

    print("\n================ RESULTATS FINAUX (OPENAI SDK) ================")
    print(f"Sujet traité : {contexte_partage.task}")
    print(f"Cycles d'itérations : {contexte_partage.revision_count}")
    print(f"Statut d'approbation : {contexte_partage.approved}")
    print(f"Dernier commentaire enregistré : {contexte_partage.feedback}")
    print(f"\nSynthèse finale renvoyée par le Runner : \n--> {resultat.final_output}")

if __name__ == "__main__":
    asyncio.run(main())