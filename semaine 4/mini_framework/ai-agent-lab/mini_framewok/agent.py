# mini_framework/agent.py
"""
Orchestrateur de la boucle d'exécution ReAct avec isolation des erreurs.
"""

import logging
from typing import Optional, Dict, Any
from openai import OpenAI
from mini_framework.config import AgentConfig
from mini_framework.message import Message
from mini_framework.conversation import Conversation
from mini_framework.registry import ToolRegistry
from mini_framework.exceptions import MaxTurnsExceededError, AgentExecutionError

logger = logging.getLogger("MiniFrameworkAgent")

class Agent:
    """Orchestrateur gérant la boucle d'exécution de décision ReAct."""
    def __init__(self, config: AgentConfig, registry: ToolRegistry):
        self.config = config
        self.registry = registry
        # Instanciation explicite du client OpenAI avec notre clé validée
        self.client = OpenAI(api_key=self.config.api_key)

    def run(self, user_prompt: str, system_prompt: str = "Vous êtes un assistant IA utile.", conversation: Optional[Conversation] = None) -> Conversation:
        """
        Exécute la boucle ReAct de manière séquentielle et sécurisée.
        """
        if conversation is None:
            conversation = Conversation()

        # Initialisation du fil conversationnel
        if not conversation.messages:
            conversation.add_message(Message(role="system", content=system_prompt))
            
        conversation.add_message(Message(role="user", content=user_prompt))

        for turn in range(self.config.max_turns):
            schemas = self.registry.get_schemas()
            
            # Paramètres de requêtage standards
            api_params: Dict[str, Any] = {
                "model": self.config.model,
                "temperature": self.config.temperature,
                "messages": conversation.get_api_payload()
            }
            if schemas:
                api_params["tools"] = schemas

            try:
                # Appel direct à l'API OpenAI
                completion = self.client.chat.completions.create(**api_params)
                choice = completion.choices
                llm_message = choice.message
            except Exception as e:
                raise AgentExecutionError(f"Échec de communication avec le fournisseur LLM : {str(e)}")

            # Extraction et normalisation des appels d'outils
            tool_calls_payload = None
            if hasattr(llm_message, "tool_calls") and llm_message.tool_calls:
                tool_calls_payload = [
                    {
                        "id": tc.id,
                        "type": "function",
                        "function": {
                            "name": tc.function.name,
                            "arguments": tc.function.arguments
                        }
                    }
                    for tc in llm_message.tool_calls
                ]

            # Enregistrement de la décision de l'agent
            conversation.add_message(Message(
                role="assistant", 
                content=llm_message.content, 
                tool_calls=tool_calls_payload
            ))

            # Si le modèle ne demande aucun outil, nous avons notre synthèse finale
            if not tool_calls_payload:
                return conversation

            # Exécution isolée des outils demandés
            for tc in tool_calls_payload:
                call_id = tc["id"]
                tool_name = tc["function"]["name"]
                tool_args = tc["function"]["arguments"]

                # Exécution sécurisée via le registre (intercepte les plantages de fonctions internes)
                observation = self.registry.execute(tool_name, tool_args)

                # Ajout de l'observation ou de l'erreur formatée au fil conversationnel
                conversation.add_message(Message(
                    role="tool",
                    content=observation,
                    name=tool_name,
                    tool_call_id=call_id
                ))

        # Si nous sortons de la boucle sans return, c'est que nous avons dépassé la limite de tours configurée
        raise MaxTurnsExceededError(
            f"L'agent a dépassé la limite de sécurité de {self.config.max_turns} tours de décision sans finaliser sa tâche."
        )