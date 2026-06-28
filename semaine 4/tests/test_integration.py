# tests/test_integration.py
"""
Suite de tests d'intégration globale pour la validation unifiée
du package industrialisé 'mini_framework'.
"""

import pytest
import json
from unittest.mock import MagicMock, patch
from mini_framework import (
    AgentConfig,
    ToolRegistry,
    Agent,
    Conversation,
    ConfigurationError,
    MaxTurnsExceededError,
    tool
)

def test_exception_configuration_manquante():
    """Vérifie que l'initialisation de la configuration échoue proprement si aucune clé n'est fournie."""
    with patch.dict("os.environ", {}, clear=True):
        with pytest.raises(ConfigurationError, match="La clé d'API OpenAI est introuvable"):
            AgentConfig(api_key="")


@patch("mini_framework.agent.OpenAI")
def test_integration_globale_boucle_react(mock_openai_class):
    """
    Simule une exécution complète et validée impliquant :
    l'initialisation de configuration, l'enregistrement d'un outil local,
    l'appel simulé de l'API OpenAI, l'exécution de l'outil et la réponse finale.
    """
    # 1. Mocking de l'API OpenAI
    mock_client = MagicMock()
    mock_openai_class.return_value = mock_client

    # Simulation Tour 1 : Demande de calcul
    mock_choice_1 = MagicMock()
    mock_choice_1.message.content = "Je dois calculer la racine carrée."
    mock_tc = MagicMock()
    mock_tc.id = "call_racine_01"
    mock_tc.function.name = "calculer_racine"
    mock_tc.function.arguments = '{"nombre": 16}'
    mock_choice_1.message.tool_calls = [mock_tc]

    # Simulation Tour 2 : Synthèse finale
    mock_choice_2 = MagicMock()
    mock_choice_2.message.content = "La racine carrée de 16 est 4."
    mock_choice_2.message.tool_calls = None

    mock_completion_1 = MagicMock()
    mock_completion_1.choices = [mock_choice_1]
    mock_completion_2 = MagicMock()
    mock_completion_2.choices = [mock_choice_2]
    
    mock_client.chat.completions.create.side_effect = [mock_completion_1, mock_completion_2]

    # 2. Définition et Enregistrement de l'outil
    registry = ToolRegistry()

    @registry.register
    def calculer_racine(nombre: int) -> dict:
        """
        Calcule la racine carrée d'un entier.
        
        Args:
            nombre: La valeur numérique cible.
        """
        import math
        return {"resultat": int(math.sqrt(nombre))}

    # 3. Initialisation de la configuration de production
    config = AgentConfig(api_key="sk-test-valid-key", max_turns=5)
    agent = Agent(config=config, registry=registry)

    # 4. Lancement de la requête
    conversation = agent.run("Calcule la racine carrée de 16")

    # 5. Assertions de robustesse globales
    assert len(conversation.messages) == 5
    assert conversation.messages.role == "system"
    assert conversation.messages.[1]role == "user"
    
    # Validation du premier tour (Thought/Action)
    assert conversation.messages.[2]role == "assistant"
    assert conversation.messages.[2]tool_calls["function"]["name"] == "calculer_racine"
    
    # Validation de l'observation locale
    assert conversation.messages.[3]role == "tool"
    assert json.loads(conversation.messages.[3]content) == {"resultat": 4}
    
    # Validation de la réponse finale
    assert conversation.messages.[4]role == "assistant"
    assert "La racine carrée de 16 est 4." in conversation.messages.[4]content


@patch("mini_framework.agent.OpenAI")
def test_integration_detection_depassement_de_tours(mock_openai_class):
    """Vérifie que l'orchestrateur lève une exception d'exécution si l'agent boucle indéfiniment."""
    mock_client = MagicMock()
    mock_openai_class.return_value = mock_client

    # Simulation d'un modèle qui demande sans cesse un outil fictif
    mock_choice = MagicMock()
    mock_choice.message.content = "Je veux encore appeler l'outil."
    mock_tc = MagicMock()
    mock_tc.id = "call_loop_01"
    mock_tc.function.name = "fictif"
    mock_tc.function.arguments = '{}'
    mock_choice.message.tool_calls = [mock_tc]

    mock_completion = MagicMock()
    mock_completion.choices = [mock_choice]
    
    # L'API répond indéfiniment par des appels d'outils
    mock_client.chat.completions.create.return_value = mock_completion

    registry = ToolRegistry()
    @registry.register
    def fictif() -> str:
        return "rien"

    # Configuration avec une limite stricte de 2 tours pour le test
    config = AgentConfig(api_key="sk-test-valid-key", max_turns=2)
    agent = Agent(config=config, registry=registry)

    # L'orchestrateur doit lever une MaxTurnsExceededError de façon contrôlée
    with pytest.raises(MaxTurnsExceededError, match="L'agent a dépassé la limite de sécurité"):
        agent.run("S'il te plaît, boucle")