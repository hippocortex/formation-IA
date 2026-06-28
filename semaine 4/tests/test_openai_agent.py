# tests/test_openai_agent.py
"""
Suite de tests unitaires pour la validation du workflow Writer-Critic
sous l'OpenAI Agents SDK.
"""

import pytest
from examples.writer_critic_openai_sdk import writer_agent, critic_agent, ProjectContext

def test_structure_et_nommage_agents():
    """Vérifie que les agents sont correctement configurés et typés."""
    assert writer_agent.name == "Writer"
    assert critic_agent.name == "Critic"
    
    # Vérification que les outils attendus sont attachés aux agents
    assert len(writer_agent.tools) == 1
    assert len(critic_agent.tools) == 1

def test_resolution_circularite_handoffs():
    """S'assure que le câblage bidirectionnel des handoffs est opérationnel."""
    # Le Writer doit avoir le Critic dans sa liste de handoffs
    assert critic_agent in writer_agent.handoffs
    
    # Le Critic doit avoir le Writer dans sa liste de handoffs
    assert writer_agent in critic_agent.handoffs

def test_manipulation_contexte():
    """Valide la structure et l'initialisation du contexte mutable."""
    ctx = ProjectContext(task="Test Unitaire")
    assert ctx.task == "Test Unitaire"
    assert ctx.draft == ""
    assert ctx.revision_count == 0
    assert ctx.approved is False