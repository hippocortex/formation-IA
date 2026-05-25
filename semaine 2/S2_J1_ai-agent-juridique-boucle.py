from typing import Dict, List, Optional
import anthropic
import json

class AgentJuridiqueIA:
    def __init__(self, api_key: str):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.historique_conversation = []
        self.contexte_utilisateur = {}
        
    def construire_prompt_systeme(self) -> str:
        return """Tu es un agent IA spécialisé en droit du travail français pour un cabinet d'avocats.

RÈGLES IMPÉRATIVES :
- Tu fournis uniquement des informations juridiques GÉNÉRALES
- Tu ne donnes JAMAIS de conseil juridique personnalisé
- Tu rappelles systématiquement que seul un avocat peut analyser une situation spécifique
- Tu inclus toujours un disclaimer sur la nature informative de tes réponses
- Tu recommandes la consultation d'un avocat pour tout cas concret

OUTILS DISPONIBLES :
Tu peux utiliser ces fonctions en les appelant dans ta réponse :

1. calculer_indemnites(anciennete_annees, salaire_brut_mensuel, type_licenciement)
   - Calcule les indemnités légales minimales
   - type_licenciement: "economique" ou "personnel"

2. proposer_rendez_vous(specialite)
   - Propose des créneaux avec un avocat
   - specialite: "droit_travail", "droit_commercial", etc.

Pour utiliser un outil, réponds avec ce format JSON :
{
  "action": "nom_fonction",
  "parametres": {...},
  "message_utilisateur": "ton message au client"
}

DÉMARCHE :
1. Accueillir et écouter la situation
2. Poser des questions de qualification si nécessaire
3. Fournir des informations générales
4. Calculer si demandé et données suffisantes
5. Recommander un avocat
6. Proposer un rendez-vous si le client est intéressé

Sois empathique, professionnel et précis."""

    def calculer_indemnites_licenciement(
        self, 
        anciennete_annees: float, 
        salaire_brut_mensuel: float,
        type_licenciement: str = "economique"
    ) -> Dict:
        """Calcul des indemnités légales minimales de licenciement"""
        
        # Indemnité légale de licenciement
        if anciennete_annees < 10:
            indemnite_legale = (anciennete_annees * 0.25) * salaire_brut_mensuel
        else:
            indemnite_legale = (10 * 0.25 + (anciennete_annees - 10) * 0.33) * salaire_brut_mensuel
        
        # Préavis (simplifié)
        if anciennete_annees < 2:
            preavis_mois = 1
        else:
            preavis_mois = 2
        
        indemnite_preavis = preavis_mois * salaire_brut_mensuel
        
        return {
            "anciennete": anciennete_annees,
            "salaire_brut": salaire_brut_mensuel,
            "type_licenciement": type_licenciement,
            "indemnite_legale": round(indemnite_legale, 2),
            "indemnite_preavis": round(indemnite_preavis, 2),
            "total_minimum": round(indemnite_legale + indemnite_preavis, 2)
        }
    
    def proposer_rendez_vous(self, specialite: str = "droit_travail") -> Dict:
        """Simule la proposition de créneaux de rendez-vous"""
        # En production, ceci interrogerait un vrai système de calendrier
        return {
            "specialite": specialite,
            "avocat": "Maître Sophie Dupont",
            "creneaux": [
                {"date": "2025-10-24", "heure": "14:00"},
                {"date": "2025-10-25", "heure": "10:30"},
                {"date": "2025-10-28", "heure": "16:00"}
            ],
            "duree": "45 minutes",
            "tarif": "150 € TTC"
        }
    
    def executer_action(self, action: str, parametres: Dict) -> Dict:
        """Exécute une action demandée par l'agent"""
        if action == "calculer_indemnites":
            return self.calculer_indemnites_licenciement(**parametres)
        elif action == "proposer_rendez_vous":
            return self.proposer_rendez_vous(**parametres)
        else:
            return {"erreur": f"Action inconnue: {action}"}
    
    def traiter_demande(self, message_utilisateur: str) -> tuple[str, Optional[Dict]]:
        """
        Traite la demande de l'utilisateur avec l'agent IA
        Retourne: (message_agent, resultat_action_si_executee)
        """
        
        # Ajouter le message utilisateur à l'historique
        self.historique_conversation.append({
            "role": "user",
            "content": message_utilisateur
        })
        
        # Appel au LLM
        response = self.client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=2000,
            system=self.construire_prompt_systeme(),
            messages=self.historique_conversation
        )
        
        reponse_agent = response.content[0].text
        
        # Vérifier si l'agent demande d'exécuter une action
        resultat_action = None
        try:
            # Tenter de parser si c'est un appel d'action JSON
            if "{" in reponse_agent and "action" in reponse_agent:
                # Extraire le JSON (simpliste, en prod utiliser un parser robuste)
                debut_json = reponse_agent.find("{")
                fin_json = reponse_agent.rfind("}") + 1
                json_str = reponse_agent[debut_json:fin_json]
                action_data = json.loads(json_str)
                
                if "action" in action_data:
                    # Exécuter l'action
                    resultat_action = self.executer_action(
                        action_data["action"],
                        action_data.get("parametres", {})
                    )
                    
                    # Construire la réponse avec le résultat
                    message_final = action_data.get("message_utilisateur", "")
                    
                    # Ajouter le résultat au contexte pour le prochain tour
                    self.historique_conversation.append({
                        "role": "assistant",
                        "content": f"{message_final}\n\nRésultat du calcul: {json.dumps(resultat_action, ensure_ascii=False)}"
                    })
                    
                    return message_final, resultat_action
        except:
            pass  # Si ce n'est pas un JSON valide, traiter comme réponse normale
        
        # Réponse normale sans action
        self.historique_conversation.append({
            "role": "assistant",
            "content": reponse_agent
        })
        
        return reponse_agent, resultat_action


# ============================================
# BOUCLE D'ÉCHANGE INTERACTIVE - VERSION CLI
# ============================================

def boucle_conversation_cli():
    """
    Boucle de conversation en ligne de commande
    C'est ICI que se passe la vraie interaction multi-tours
    """
    print("=" * 60)
    print("Agent IA Juridique - Cabinet d'Avocats")
    print("=" * 60)
    print("Tapez 'exit' ou 'quit' pour terminer la conversation\n")
    
    agent = AgentJuridiqueIA(api_key="votre_cle_api")
    
    # Message d'accueil initial
    print("🤖 Agent: Bonjour, je suis l'assistant virtuel du cabinet.")
    print("         Comment puis-je vous aider aujourd'hui ?\n")
    
    # BOUCLE INFINIE jusqu'à ce que l'utilisateur quitte
    while True:
        # Récupérer l'entrée utilisateur
        message_utilisateur = input("👤 Vous: ").strip()
        
        # Condition de sortie
        if message_utilisateur.lower() in ['exit', 'quit', 'sortir', 'au revoir']:
            print("\n🤖 Agent: Au revoir ! N'hésitez pas à nous recontacter.")
            break
        
        if not message_utilisateur:
            continue
        
        # Traiter le message avec l'agent
        print("\n🤖 Agent: ", end="", flush=True)
        reponse, action_resultat = agent.traiter_demande(message_utilisateur)
        
        # Afficher la réponse
        print(reponse)
        
        # Si une action a été exécutée, afficher le résultat formaté
        if action_resultat:
            print("\n📊 Résultat du calcul:")
            for cle, valeur in action_resultat.items():
                print(f"   • {cle}: {valeur}")
        
        print()  # Ligne vide pour la lisibilité


# ============================================
# BOUCLE D'ÉCHANGE - VERSION SCRIPT SIMULÉ
# ============================================

def simulation_conversation_complete():
    """
    Simule une conversation complète sans interaction CLI
    Utile pour tests et démonstrations
    """
    agent = AgentJuridiqueIA(api_key="votre_cle_api")
    
    # Liste des messages à échanger
    messages_utilisateur = [
        "Bonjour, mon employeur vient de me licencier après 5 ans d'ancienneté. Ai-je droit à des indemnités ?",
        "C'est un licenciement économique. Mon salaire brut est de 2 800 € par mois.",
        "Oui, je souhaite prendre rendez-vous.",
        "Le créneau du vendredi 25 octobre à 10h30 me convient parfaitement."
    ]
    
    print("=" * 70)
    print("SIMULATION DE CONVERSATION COMPLÈTE")
    print("=" * 70)
    print()
    
    # BOUCLE sur chaque message
    for i, message in enumerate(messages_utilisateur, 1):
        print(f"👤 Client (tour {i}): {message}")
        print()
        
        # L'agent traite le message
        reponse, action_resultat = agent.traiter_demande(message)
        
        print(f"🤖 Agent (tour {i}): {reponse}")
        
        if action_resultat:
            print("\n📊 Calcul effectué:")
            print(json.dumps(action_resultat, indent=2, ensure_ascii=False))
        
        print("\n" + "-" * 70 + "\n")
    
    print("✅ Conversation terminée avec succès")
    print(f"📝 Nombre total d'échanges dans l'historique: {len(agent.historique_conversation)}")


# ============================================
# BOUCLE D'ÉCHANGE - VERSION WEB/API
# ============================================

class AgentJuridiqueWeb:
    """
    Version adaptée pour une API web (FastAPI, Flask, etc.)
    Gère les sessions utilisateur avec stockage de l'historique
    """
    
    def __init__(self):
        self.sessions = {}  # Stockage des sessions {session_id: agent}
    
    def creer_session(self, session_id: str, api_key: str) -> str:
        """Crée une nouvelle session de conversation"""
        self.sessions[session_id] = AgentJuridiqueIA(api_key)
        return session_id
    
    def traiter_message(self, session_id: str, message: str) -> Dict:
        """
        Traite un message dans le contexte d'une session
        Retourne JSON pour l'API
        """
        if session_id not in self.sessions:
            return {
                "erreur": "Session inconnue",
                "code": 404
            }
        
        agent = self.sessions[session_id]
        reponse, action_resultat = agent.traiter_demande(message)
        
        return {
            "session_id": session_id,
            "reponse_agent": reponse,
            "action_executee": action_resultat,
            "nombre_echanges": len(agent.historique_conversation),
            "timestamp": "2025-10-22T11:30:00"
        }
    
    def terminer_session(self, session_id: str):
        """Termine et nettoie une session"""
        if session_id in self.sessions:
            del self.sessions[session_id]


# Exemple d'utilisation avec FastAPI (pseudo-code)
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()
agent_web = AgentJuridiqueWeb()

class Message(BaseModel):
    session_id: str
    message: str

@app.post("/nouvelle-session")
def nouvelle_session():
    import uuid
    session_id = str(uuid.uuid4())
    agent_web.creer_session(session_id, "votre_cle_api")
    return {"session_id": session_id}

@app.post("/message")
def envoyer_message(msg: Message):
    # LA BOUCLE se passe côté client qui appelle cette API
    # à chaque nouveau message de l'utilisateur
    resultat = agent_web.traiter_message(msg.session_id, msg.message)
    return resultat

@app.post("/terminer-session")
def terminer_session(session_id: str):
    agent_web.terminer_session(session_id)
    return {"status": "session terminée"}
"""


# ============================================
# POINT D'ENTRÉE PRINCIPAL
# ============================================

if __name__ == "__main__":
    print("Choisissez le mode d'exécution:")
    print("1. Conversation interactive CLI")
    print("2. Simulation de conversation complète")
    
    choix = input("\nVotre choix (1 ou 2): ").strip()
    
    if choix == "1":
        boucle_conversation_cli()
    elif choix == "2":
        simulation_conversation_complete()
    else:
        print("Choix invalide")
