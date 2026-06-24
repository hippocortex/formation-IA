# tests/test_graph.py
import pytest
from mini_framework.state import AgentState
from mini_framework.graph import StateGraph

def test_validation_graphe_sans_entree():
    """Vérifie qu'un graphe sans point d'entrée lève une exception lors de la compilation."""
    graph = StateGraph()
    graph.add_node("N1", lambda s: {})
    
    with pytest.raises(ValueError, match="Le graphe doit obligatoirement posséder un point d'entrée"):
        graph.compile()

def test_transition_lineaire_determininiste():
    """Valide l'ordre de passage d'un flux linéaire simple à deux nœuds."""
    graph = StateGraph(state_schema=dict)
    
    def noeud_un(state: dict) -> dict:
        return {"valeur": 10}
        
    def noeud_deux(state: dict) -> dict:
        return {"valeur": state["valeur"] * 2}

    graph.add_node("Un", noeud_un)
    graph.add_node("Deux", noeud_deux)
    graph.set_entry_point("Un")
    graph.add_edge("Un", "Deux")
    
    compiled = graph.compile()
    state_result = compiled.invoke({"valeur": 0})
    
    assert state_result["valeur"] == 20

def test_boucle_avec_arret_conditionnel():
    """Valide le fonctionnement d'une boucle conditionnelle s'arrêtant au bon moment."""
    graph = StateGraph(state_schema=dict)
    
    def incrementer(state: dict) -> dict:
        return {"compteur": state.get("compteur", 0) + 1}
        
    def aiguiller(state: dict) -> str:
        return "continuer" if state["compteur"] < 3 else "arreter"

    graph.add_node("Increment", incrementer)
    graph.set_entry_point("Increment")
    
    graph.add_conditional_edges(
        from_node="Increment",
        condition=aiguiller,
        path_map={
            "continuer": "Increment",
            "arreter": None
        }
    )
    
    compiled = graph.compile()
    res = compiled.invoke({"compteur": 0})
    
    assert res["compteur"] == 3