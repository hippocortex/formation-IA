# examples/writer_critic_graph.py
from mini_framework.state import AgentState
from mini_framework.graph import StateGraph

# ==========================================
# 1. Définition des Nœuds fonctionnels
# ==========================================

def node_writer(state: AgentState) -> dict:
    """Simule le travail d'un agent de rédaction."""
    revision = state.revision_count + 1
    
    if state.feedback:
        # S'il y a des retours, on adapte le brouillon
        new_draft = f"Article (Version {revision}) : Contenu de haute qualité traitant de '{state.task}', intégrant les corrections demandées : {state.feedback}."
    else:
        # Premier essai de rédaction
        new_draft = f"Article (Version {revision}) : Brouillon brut au sujet de '{state.task}'."
        
    return {
        "draft": new_draft,
        "revision_count": revision
    }

def node_critic(state: AgentState) -> dict:
    """Simule le travail d'un agent de relecture critique."""
    # Simulation d'une validation uniquement à partir de la version 3 pour forcer un cycle d'écriture
    if state.revision_count >= 3:
        return {
            "approved": True,
            "feedback": "Excellent travail. L'article répond parfaitement aux exigences du guide de style."
        }
    else:
        # Demande de corrections
        return {
            "approved": False,
            "feedback": f"Le brouillon manque de profondeur technique (Revue effectuée à la révision {state.revision_count})."
        }

# ==========================================
# 2. Définition de l'Aiguillage conditionnel
# ==========================================

def condition_decision(state: AgentState) -> str:
    """Fonction d'analyse guidant la transition d'état."""
    if state.approved:
        return "approuve"
    else:
        return "a_corriger"

# ==========================================
# 3. Assemblage et compilation du Graphe
# ==========================================

workflow = StateGraph(state_schema=AgentState)

# Enregistrement des nœuds
workflow.add_node("Writer", node_writer)
workflow.add_node("Critic", node_critic)

# Configuration de la séquence
workflow.set_entry_point("Writer")

# Le rédacteur envoie systématiquement son travail au critique
workflow.add_edge("Writer", "Critic")

# Le critique oriente la suite selon l'état d'approbation de l'article
workflow.add_conditional_edges(
    from_node="Critic",
    condition=condition_decision,
    path_map={
        "approuve": None,          # L'arrêt est représenté par None (END)
        "a_corriger": "Writer"     # Retour à l'étape d'écriture
    }
)

# Compilation
app_graphe = workflow.compile()

# ==========================================
# 4. Lancement de la simulation
# ==========================================
if __name__ == "__main__":
    # État initial de départ
    state_depart = AgentState(task="Les bases du Model Context Protocol en 2026")
    
    # Exécution du processus
    state_final = app_graphe.invoke(state_depart)
    
    print("\n================ RESULTATS FINAUX ================")
    print(f"Sujet initial : {state_final.task}")
    print(f"Nombre total de révisions nécessaires : {state_final.revision_count}")
    print(f"Statut d'approbation : {state_final.approved}")
    print(f"Dernier feedback reçu : {state_final.feedback}")
    print(f"Contenu final de l'article : \n--> {state_final.draft}")