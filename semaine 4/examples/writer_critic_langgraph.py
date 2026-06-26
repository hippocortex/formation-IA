# examples/writer_critic_langgraph.py
"""
Implémentation industrielle du workflow rédactionnel cyclique Writer-Critic
en utilisant le framework d'orchestration LangGraph.
"""

from typing import Dict, Any
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver

# ==========================================
# 1. Déclaration de la structure de l'État (State)
# ==========================================

class WriterCriticState(TypedDict):
    """
    Définit le schéma d'état de notre graphe LangGraph.
    Contrairement à notre Dataclass du Jour 3, nous utilisons ici un TypedDict standard.
    """
    task: str                         # La consigne d'origine de l'utilisateur
    draft: str                        # Le brouillon d'article actuel
    feedback: str                     # Les commentaires du relecteur
    revision_count: int               # Le nombre de cycles effectués
    approved: bool                    # Le statut d'approbation final

# ==========================================
# 2. Définition des Nœuds fonctionnels (Nodes)
# ==========================================

def node_writer(state: WriterCriticState) -> Dict[str, Any]:
    """
    Nœud représentant l'agent de rédaction (Writer).
    Il lit l'état actuel et renvoie uniquement les clés mises à jour.
    """
    # Récupération sécurisée avec valeurs par défaut
    revision = state.get("revision_count", 0) + 1
    feedback = state.get("feedback", "")
    task = state.get("task", "")

    if feedback:
        # S'il y a déjà des retours, on adapte la version
        new_draft = f"Article (Version {revision}) : Contenu de haute qualité traitant de '{task}', intégrant les corrections demandées : {feedback}."
    else:
        # Premier jet de rédaction
        new_draft = f"Article (Version {revision}) : Brouillon brut au sujet de '{task}'."

    # LangGraph prend les valeurs de retour et les fusionne dans l'état global
    return {
        "draft": new_draft,
        "revision_count": revision
    }


def node_critic(state: WriterCriticState) -> Dict[str, Any]:
    """
    Nœud représentant l'agent de relecture critique (Critic).
    """
    revision = state.get("revision_count", 0)

    # Simulation d'un cycle de relecture exigeant (approbation uniquement à la révision 3)
    if revision >= 3:
        return {
            "approved": True,
            "feedback": "Excellent travail. L'article répond parfaitement aux exigences de profondeur technique."
        }
    else:
        return {
            "approved": False,
            "feedback": f"Le brouillon manque de profondeur (Revue effectuée à la révision {revision})."
        }

# ==========================================
# 3. Définition de l'Aiguillage conditionnel (Router)
# ==========================================

def router_decision(state: WriterCriticState) -> str:
    """
    Analyse l'état courant pour guider la transition dynamique.
    Elle retourne une clé de routage qui sera mappée par le graphe.
    """
    if state.get("approved"):
        return "approved"
    else:
        return "a_corriger"

# ==========================================
# 4. Assemblage, Câblage et Compilation du Graphe
# ==========================================

# Initialisation du constructeur de graphe en lui passant notre schéma de données
workflow = StateGraph(WriterCriticState)

# Enregistrement des nœuds de traitement
workflow.add_node("Writer", node_writer)
workflow.add_node("Critic", node_critic)

# Définition des connexions (Edges)
# START est le point d'entrée virtuel officiel de LangGraph
workflow.add_edge(START, "Writer")

# Liaison déterministe linéaire : Writer transmet toujours son brouillon au Critic
workflow.add_edge("Writer", "Critic")

# Liaison conditionnelle : le Critic oriente l'exécution
workflow.add_conditional_edges(
    "Critic",                 # Nœud d'origine
    router_decision,          # Fonction logique de décision
    {
        "approved": END,      # Si approuvé, on termine le processus (END)
        "a_corriger": "Writer" # Si refusé, on renvoie au Writer pour correction
    }
)

# Configuration de la persistance via un checkpointer en mémoire
checkpointer = InMemorySaver()

# Compilation finale du graphe pour obtenir notre application exécutable
app_graphe = workflow.compile(checkpointer=checkpointer)

# ==========================================
# 5. Lancement de la Simulation
# ==========================================
if __name__ == "__main__":
    print("--- Démarrage du Workflow cyclique sous LangGraph ---")
    
    # Configuration du contexte d'exécution (obligatoire pour utiliser un checkpointer)
    config = {"configurable": {"thread_id": "session_recherche_mcp_123"}}
    
    # État d'entrée initial de l'application
    etat_initial = {
        "task": "Les bases du Model Context Protocol en 2026",
        "draft": "",
        "feedback": "",
        "revision_count": 0,
        "approved": False
    }

    # Invocation de notre graphe avec état et configuration
    etat_final = app_graphe.invoke(etat_initial, config)

    print("\n================ RESULTATS FINAUX (LANGGRAPH) ================")
    print(f"Sujet traité : {etat_final['task']}")
    print(f"Cycles d'itérations : {etat_final['revision_count']}")
    print(f"Statut d'approbation : {etat_final['approved']}")
    print(f"Dernier commentaire : {etat_final['feedback']}")
    print(f"Contenu final de l'article : \n--> {etat_final['draft']}")