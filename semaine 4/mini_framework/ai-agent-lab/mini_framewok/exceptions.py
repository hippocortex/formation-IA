# mini_framework/exceptions.py
"""
Hiérarchie d'exceptions typées pour la gestion robuste des erreurs
au sein du mini-framework.
"""

class FrameworkError(Exception):
    """Exception de base de laquelle héritent toutes les erreurs du framework."""
    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class ConfigurationError(FrameworkError):
    """Levée lorsqu'une clé d'API ou une variable de configuration est manquante ou invalide."""
    pass


class AgentExecutionError(FrameworkError):
    """Exception levée lorsqu'une boucle ReAct ou un agent rencontre un échec critique."""
    pass


class MaxTurnsExceededError(AgentExecutionError):
    """Levée lorsque l'agent atteint la limite de tours maximale configurée sans résoudre la tâche."""
    pass


class ToolError(FrameworkError):
    """Levée lors d'un échec lié à l'introspection d'une fonction ou d'une mauvaise utilisation d'outil."""
    pass


class ToolExecutionError(ToolError):
    """Enveloppe et remonte de façon contrôlée une exception levée à l'intérieur d'un outil en exécution."""
    def __init__(self, tool_name: str, original_exception: Exception):
        msg = f"L'outil '{tool_name}' a provoqué une exception : {str(original_exception)}"
        super().__init__(msg)
        self.tool_name = tool_name
        self.original_exception = original_exception


class RegistryError(FrameworkError):
    """Levée lorsqu'un outil demandé est absent du registre ou possède un nom dupliqué."""
    pass