# mini_framework/graph.py
import logging
from typing import Dict, List, Any, Callable, Tuple, Optional, Union
from mini_framework.state import AgentState

# Configuration élémentaire du logger pour le suivi d'exécution
logging.basicConfig(level=logging.INFO, format="%(asctime)s - - %(message)s")
logger = logging.getLogger("StateGraph")

class StateGraph:
    """
    Moteur de workflow par graphes d'états, modélisant des flux de travail
    modulaires et cycliques basés sur des transitions déterministes et conditionnelles.
    """
    def __init__(self, state_schema: type = AgentState):
        self.state_schema = state_schema
        self.nodes: Dict[str, Callable[[Any], Dict[str, Any]]] = {}
        self.edges: List] =
        self.conditional_edges: Dict, str], Dict[str, str]]] = {}
        self.entry_point: Optional[str] = None

    def add_node(self, name: str, func: Callable[[Any], Dict[str, Any]]) -> None:
        """Enregistre un nœud fonctionnel au sein du graphe."""
        if name in self.nodes:
            raise ValueError(f"Le nœud '{name}' est déjà enregistré.")
        self.nodes[name] = func

    def set_entry_point(self, name: str) -> None:
        """Définit le point d'entrée d'exécution du graphe."""
        self.entry_point = name

    def add_edge(self, from_node: str, to_node: str) -> None:
        """Crée une transition directe et unilatérale entre deux nœuds."""
        self.edges.append((from_node, to_node))

    def add_conditional_edges(
        self, 
        from_node: str, 
        condition: Callable[[Any], str], 
        path_map: Dict[str, str]
    ) -> None:
        """
        Configure un aiguillage dynamique en fonction d'une fonction de décision.
        """
        self.conditional_edges[from_node] = (condition, path_map)

    def compile(self):
        """Valide et compile le graphe pour le rendre exécutable."""
        if not self.entry_point:
            raise ValueError("Le graphe doit obligatoirement posséder un point d'entrée (set_entry_point).")
        for edge_from, edge_to in self.edges:
            if edge_from not in self.nodes or edge_to not in self.nodes:
                raise ValueError(f"Transition invalide : l'un des nœuds de l'arête ({edge_from} -> {edge_to}) n'existe pas.")
        return CompiledGraph(self)


class CompiledGraph:
    """Runtime d'exécution d'un graphe d'états compilé."""
    def __init__(self, graph: StateGraph):
        self.graph = graph

    def invoke(self, initial_state: Any, max_steps: int = 20) -> Any:
        """
        Exécute le workflow de nœuds en nœuds jusqu'à l'arrêt ou le dépassement des étapes.
        """
        state = initial_state
        current_node = self.graph.entry_point
        step = 0

        logger.info("--- Début de l'exécution du Graphe d'États ---")

        while current_node and step < max_steps:
            step += 1
            logger.info(f"Étape {step} : Activation du nœud [{current_node}]")
            
            # 1. Appel du nœud
            node_func = self.graph.nodes[current_node]
            updates = node_func(state)

            # 2. Application des mises à jour de façon sécurisée à l'état partagé
            if updates:
                for key, val in updates.items():
                    if hasattr(state, key):
                        setattr(state, key, val)
                    elif isinstance(state, dict):
                        state[key] = val

            # 3. Résolution du nœud suivant (Routage)
            next_node = None

            # Cas A : Aiguillage conditionnel
            if current_node in self.graph.conditional_edges:
                condition_func, path_map = self.graph.conditional_edges[current_node]
                decision = condition_func(state)
                next_node = path_map.get(decision)
                logger.info(f"Aiguillage conditionnel de [{current_node}] -> Décision : '{decision}' -> Prochain nœud : [{next_node}]")
            
            # Cas B : Transition linéaire standard
            else:
                transitions = [to for frm, to in self.graph.edges if frm == current_node]
                if transitions:
                    next_node = transitions # Transition unique
                    logger.info(f"Transition déterministe de [{current_node}] -> Prochain nœud : [{next_node}]")

            current_node = next_node

        if step >= max_steps:
            logger.warning(f"Arrêt forcé : dépassement du nombre maximal d'étapes de sécurité ({max_steps}).")

        logger.info("--- Fin de l'exécution du Graphe d'États ---")
        return state