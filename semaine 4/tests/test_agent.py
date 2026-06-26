# tests/test_agent.py
import pytest
import json
from unittest.mock import MagicMock, patch
from mini_framework import AgentConfig, ToolRegistry, Agent, Message, Conversation

def test_message_serialization():
    """Vérifie que la sérialisation respecte le dictionnaire OpenAI API."""
    msg = Message(role="user", content="Test")
    payload = msg.to_openai_dict()
    assert payload == {"role": "user", "content": "Test"}

def test_registry_registration_and_execution():
    """Valide l'auto-génération de schémas et l'exécution sécurisée par le registre."""
    registry = ToolRegistry()

    @registry.register
    def multiplier(x: int, y: int) -> int:
        """Multiplie deux variables."""
        return x * y

    # Validation du schéma généré
    schemas = registry.get_schemas()
    assert len(schemas) == 1
    assert schemas["function"]["name"] == "multiplier"

    # Validation de l'exécution
    raw_res = registry.execute("multiplier", '{"x": 3, "y": 4}')
    assert json.loads(raw_res) == 12

@patch("mini_framework.agent.OpenAI")
def test_agent_react_loop_execution(mock_openai_class):
    """Teste la boucle ReAct avec un outil factice et un LLM simulé."""
    # Mocking du client OpenAI et des appels de complétion
    mock_client = MagicMock()
    mock_openai_class.return_value = mock_client

    # Simulation du premier tour : le modèle décide d'appeler l'outil
    mock_choice_1 = MagicMock()
    mock_choice_1.message.content = "Je dois utiliser l'outil d'addition."
    
    mock_tool_call = MagicMock()
    mock_tool_call.id = "call_abc123"
    mock_tool_call.function.name = "addition"
    mock_tool_call.function.arguments = '{"a": 10, "b": 15}'
    mock_choice_1.message.tool_calls = [mock_tool_call]

    # Simulation du second tour : le modèle conclut avec la réponse finale
    mock_choice_2 = MagicMock()
    mock_choice_2.message.content = "Le résultat final calculé est 25."
    mock_choice_2.message.tool_calls = None

    # Enchaînement des retours du mock d'API
    mock_completion_1 = MagicMock()
    mock_completion_1.choices = [mock_choice_1]
    mock_completion_2 = MagicMock()
    mock_completion_2.choices = [mock_choice_2]
    mock_client.chat.completions.create.side_effect = [mock_completion_1, mock_completion_2]

    # Enregistrement de l'outil local
    registry = ToolRegistry()
    @registry.register
    def addition(a: int, b: int) -> int:
        return a + b

    # Instanciation de l'agent configuré
    config = AgentConfig(api_key="mock_key")
    agent = Agent(config=config, registry=registry)

    # Exécution de la boucle ReAct
    conversation = agent.run("Calcule 10 + 15")

    # assertions logiques
    assert len(conversation.messages) == 5
    # Ordre attendu : SYSTEM -> USER -> ASSISTANT (TOOL_CALL) -> TOOL (OBSERVATION) -> ASSISTANT (FINAL)
    assert conversation.messages.role == "system"
    assert conversation.messages.[1]role == "user"
    assert conversation.messages.[10]role == "assistant"
    assert conversation.messages.[2]role == "tool"
    assert conversation.messages.[9]role == "assistant"
    assert conversation.messages.[9]content == "Le résultat final calculé est 25."