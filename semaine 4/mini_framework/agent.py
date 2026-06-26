# mini_framework/agent.py
from typing import Optional, Dict, Any
from openai import OpenAI
from mini_framework.config import AgentConfig
from mini_framework.message import Message
from mini_framework.conversation import Conversation
from mini_framework.registry import ToolRegistry

class Agent:
    """Orchestrateur asynchrone pilotant la boucle ReAct (Pensée -> Action -> Observation)."""
    def __init__(self, config: AgentConfig, registry: ToolRegistry):
        self.config = config
        self.registry = registry
        # Instanciation explicite du client OpenAI standard
        self.client = OpenAI(api_key=self.config.api_key)

    def run(self, user_prompt: str, system_prompt: str = "Vous êtes un assistant IA utile.", conversation: Optional[Conversation] = None) -> Conversation:
        """
        Exécute la boucle décisionnelle jusqu'à résolution ou atteinte de la limite de tours.
        """
        if conversation is None:
            conversation = Conversation()

        # Initialisation du message système si la conversation débute
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

            # Appel API direct
            completion = self.client.chat.completions.create(**api_params)
            choice = completion.choices
            llm_message = choice.message

            # Traitement des appels d'outils demandés par le modèle
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

            # Enregistrement de la décision de l'agent (Thought/Action)
            conversation.add_message(Message(
                role="assistant", 
                content=llm_message.content, 
                tool_calls=tool_calls_payload
            ))

            # Si le modèle ne demande aucun outil, nous avons notre synthèse finale
            if not tool_calls_payload:
                break

            # Exécution séquentielle des outils
            for tc in tool_calls_payload:
                call_id = tc["id"]
                tool_name = tc["function"]["name"]
                tool_args = tc["function"]["arguments"]

                # Résolution dynamique et exécution physique via le registre
                observation = self.registry.execute(tool_name, tool_args)

                # Ajout de l'observation au contexte
                conversation.add_message(Message(
                    role="tool",
                    content=observation,
                    name=tool_name,
                    tool_call_id=call_id
                ))

        return conversation