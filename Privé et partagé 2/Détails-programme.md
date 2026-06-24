# Détails

---

## Rappel — Semaine 1 (inchangée)

Tu as indiqué que tu as *déjà* commencé cette semaine. Rappel synthétique :

- Types de modèles (GPT, BERT, T5, autoregressif vs encoder-decoder)
- Prompt engineering (bases)
- Techniques avancées (few-shot, CoT, prompt patterns)
- Mini-projet / revue & consolidation

Je ne touche pas à cette semaine.

---

## Nouveau plan (Semaine 2 → Semaine 8), 1h par jour — réordonné selon tes priorités

### Semaine 2 — Agents IA : Fondations & API (1h/jour)

Objectif : maîtriser les building blocks des agents (function calling, tool use, sessions).

1. Jour 1 — Vue d’ensemble agents vs LLM : architectures, cas d’usage, limits. (Lecture + 20m pratique)
2. Jour 2 — OpenAI Function Calling / Responses API : schemas JSON, function definitions. (Tutoriel + 20m test)
3. Jour 3 — Implémenter un agent simple (local mock) : get_weather / create_event. (Code)
4. Jour 4 — Gestion de dialogue & session (conversation state) : stratégie pour conserver contexte court. (Exos)
5. Jour 5 — Ajout d’un outil externe (search / docs) : connecter un search mock / appels HTTP. (Intégration)
6. Jour 6 — Tests et défenses (input sanitization, refus policy). (Checklist + mini tests)
7. Jour 7 — Revue & amélioration : nettoyer le prototype, noter questions pour multi-agent. (Refactor)

---

### Semaine 3 — Multi-agent & protocole MCP (pratique)

Objectif : comprendre MCP et implémenter échanges inter-agents.

1. Jour 1 — Concepts multi-agent : rôles (analyst, planner, executor, arbiter).
2. Jour 2 — Introduction MCP : objectifs et message format (lecture + notes).
3. Jour 3 — Implémenter un échange MCP minimal (HTTP ou message bus mock).
4. Jour 4 — Coordination & négociation : patterns (vote, consensus, arbitration).
5. Jour 5 — Sécurité inter-agents : scopes, accès aux ressources, filtres.
6. Jour 6 — Bench simple multi-agent : latence, itérations, robustesse.
7. Jour 7 — Mini-projet : 2 agents coopérants (retrieval → plan → exec) + logs.

---

### Semaine 4 — Frameworks d'Agents

Objectif : passer d’un agent ad-hoc à un agent orchestré par un framework.

---

- **J1** : Pourquoi les frameworks existent + premiers composants ✅
- **J2** : Développer un véritable mini framework (≈300 lignes de code)
- **J3** : Ajouter un moteur de workflow (`Graph`, `Node`, `Edge`, `State`) et découvrir que nous avons recréé les concepts de LangGraph.
- **J4** : Réimplémenter le même projet avec **LangGraph**.
- **J5** : Réimplémenter le même projet avec **OpenAI Agents SDK**.
- **J6** : Comparer **CrewAI**, **Google ADK** et **AutoGen**.
- **J7** : Refactoriser le mini framework en un projet complet.

# Semaine 5 — Concevoir une architecture IA prête pour la production

> **Question de la semaine :**
> 
> 
> *Comment transformer un prototype d'agent en un service fiable, sécurisé et scalable ?*
> 

---

## Jour 1 — Architecturer un système IA moderne

### Théorie

- Pourquoi une architecture IA est différente d'un backend REST classique
- Les composants d'un système agentique
- Stateless vs Stateful
- Gestion des sessions
- Où vivent les conversations ?
- Où vivent les agents ?

### Architecture étudiée

```
Utilisateur
      │
      ▼
API Gateway
      │
      ▼
FastAPI
      │
      ▼
Agent
      │
 ┌────┼──────────┐
 ▼    ▼          ▼
MCP Redis PostgreSQL
 │
 ▼
LLM
```

### Atelier

Dessiner ton architecture cible.

---

## Jour 2 — Concevoir une API pour des agents

Question :

> Comment expose-t-on un agent ?
> 

On verra :

- REST
- Streaming
- SSE
- WebSocket
- Sessions
- Authentification
- Gestion des quotas
- Token Budget
- API versioning

Projet :

Créer une API FastAPI propre.

---

## Jour 3 — Déploiement : quelles options choisir ?

Question :

> Dois-je héberger moi-même ou utiliser une plateforme ?
> 

Comparaison :

- Docker
- FastAPI
- OpenAI Hosted
- Azure AI Foundry
- Google Vertex AI
- AWS Bedrock
- Serverless

Exercice :

Dockeriser le projet.

---

## Jour 4 — Faire évoluer l'architecture

Question :

> Que se passe-t-il lorsque 1000 utilisateurs arrivent ?
> 

On parlera :

- montée en charge
- file d'attente
- workers
- Kubernetes (concepts)
- cache
- répartition des agents

Pas de YAML Kubernetes interminables, mais les principes.

---

## Jour 5 — Observabilité

Sujet souvent absent des formations.

Pourtant indispensable.

On verra :

- Logs
- Traces
- Coût des tokens
- Latence
- LangSmith
- OpenAI Tracing
- Phoenix (Arize)
- OpenTelemetry

Projet :

Ajouter un tableau de bord simple.

---

## Jour 6 — Sécurité des agents

Très orienté IA.

- Prompt Injection
- Indirect Prompt Injection
- Tool Abuse
- Secrets
- PII
- MCP Security
- Guardrails
- Validation des entrées

Projet :

Sécuriser ton agent.

---

## Jour 7 — Architecture Review

Comme dans une vraie entreprise.

Tu présenteras :

- diagrammes
- flux
- mémoire
- sécurité
- monitoring
- coûts

---

# Semaine 6 — Le RAG comme outil d'un agent

> **Question de la semaine :**
> 
> 
> *Comment permettre à un agent de raisonner sur des connaissances qu'il ne possède pas ?*
> 

---

## Jour 1 — Pourquoi le RAG aujourd'hui ?

Pas de théorie historique.

On verra :

- Pourquoi les plateformes utilisent le retrieval.
- Le RAG comme **outil** de l'agent.
- Les limites du contexte.

---

## Jour 2 — Embeddings

Seulement ce qui est utile.

- embeddings
- similarité
- cosine
- vector stores
- choix du modèle

Pas de mathématiques inutiles.

---

## Jour 3 — Construire un pipeline RAG

Pipeline moderne :

```
Question

↓

Agent

↓

Retriever

↓

Context Builder

↓

LLM
```

Projet :

Premier RAG.

---

## Jour 4 — Optimiser le Retrieval

On verra :

- Hybrid Search
- BM25
- Reranking
- Multi-query
- Context Compression

---

## Jour 5 — Évaluer un RAG

Sujet très demandé.

- Recall
- Precision
- Faithfulness
- Human Evaluation
- Benchmarks

Projet :

Construire un mini framework d'évaluation.

---

## Jour 6 — Réduire les coûts

Questions concrètes :

- Combien coûte mon RAG ?
- Comment réduire les tokens ?
- Cache
- Chunking
- Condensed Retrieval

---

## Jour 7 — Intégrer le RAG à l'agent

Le projet fil rouge évolue :

```
Utilisateur

↓

Agent

↓

Décision

↓

Tool

↓

RAG

↓

Réponse
```

---

# Semaine 7 — Workflow Engineering & Automatisation

> **Question de la semaine :**
> 
> 
> *Quand faut-il coder et quand faut-il orchestrer ?*
> 

---

## Jour 1 — Les différents types de workflows

- Synchrone
- Asynchrone
- Événementiel
- Human-in-the-loop

---

## Jour 2 — Découverte de n8n

- Philosophie
- Forces
- Limites
- Connexion avec un agent

---

## Jour 3 — Intégrer un agent dans un workflow

Exemple :

```
Email
   ↓
n8n
   ↓
Agent
   ↓
CRM
   ↓
Slack
```

---

## Jour 4 — Comparer les orchestrateurs

- n8n
- Temporal
- GitHub Actions
- Azure Logic Apps
- AWS Step Functions

Quand utiliser chacun ?

---

## Jour 5 — Human-in-the-loop

- Validation
- Escalade
- Approbation
- Relecture

---

## Jour 6 — Workflow hybride

Créer un processus mêlant :

- automatisation ;
- agent IA ;
- intervention humaine.

---

## Jour 7 — Projet métier

Construire un workflow complet (ex. traitement d'e-mails, support client, validation documentaire).

---

# Semaine 8 — Évaluation, optimisation et gouvernance

> **Question de la semaine :**
> 
> 
> *Comment garantir qu'un système IA reste fiable dans le temps ?*
> 

---

## Jour 1 — Évaluer un agent

- Critères de qualité
- Jeux de tests
- Évaluation automatique

---

## Jour 2 — Optimiser les performances

- Latence
- Parallélisme
- Cache
- Choix des modèles

---

## Jour 3 — Réduire les coûts

- Token Budget
- Modèles adaptés au besoin
- Caching des réponses
- Arbitrage coût/qualité

---

## Jour 4 — Gouvernance et conformité

- Traçabilité
- Audit
- Gestion des données
- Conformité (RGPD, conservation des données)

---

## Jour 5 — Décider : plateforme ou développement ?

Études de cas :

- OpenAI Platform
- OpenAI Agents SDK
- Google ADK
- LangGraph
- n8n
- Développement sur mesure

Objectif : apprendre à justifier un choix d'architecture.

---

## Jour 6 — Préparer un projet professionnel

- Documentation
- Diagrammes
- ADR (Architecture Decision Records)
- Démonstration

---

## Jour 7 — Soutenance technique

Présentation complète du projet fil rouge :

- architecture ;
- choix technologiques ;
- sécurité ;
- observabilité ;
- coûts ;
- évolutions possibles.

## 

Excellent 👌 tu veux donc :

- Deux notebooks (Semaine 2 et Semaine 4)
- En **deux versions chacun** :
    1. **Python pur** (sans dépendances externes)
    2. **LangChain** (architecture modulaire, outils + agents)
- Chaque version avec **2 modes d’exécution** :
    - Mode **mock local** (aucune clé API, appels simulés)
    - Mode **réel avec clé OpenAI** (test direct de l’API)

Soit **4 notebooks au total** :

| Notebook | Contenu | Stack | Mode | Objectif |
| --- | --- | --- | --- | --- |
| `S2_Agent_OpenAI_Python.ipynb` | Semaine 2 : Agents IA – fondations | Python pur | mock + API | Créer un agent unique avec tools |
| `S2_Agent_OpenAI_LangChain.ipynb` | Semaine 2 : Agents IA – fondations | LangChain | mock + API | Agent LangChain + tool HTTP |
| `S4_MultiAgent_MCP_Python.ipynb` | Semaine 4 : Multi-agent et protocole MCP | Python pur | mock + API | Multi-agent planner/executor |
| `S4_MultiAgent_MCP_LangChain.ipynb` | Semaine 4 : Multi-agent et protocole MCP | LangChain | mock + API | Multi-agent orchestration LangChain |

Chacun comportera :

- 🔹 Introduction et rappel des concepts (avec mes notes pédagogiques)
- 🔹 Cellules “Mode local” (mock complet)
- 🔹 Cellules “Mode API” avec clé OpenAI
- 🔹 Cellules d’expérimentation et d’extension (custom tool, logs, dialogues)
- 🔹 Résumé et exercices proposés

Souhaites-tu que je :

👉 les **génère maintenant (4 fichiers `.ipynb`)** prêts à télécharger,

ou que je te montre **le contenu complet du premier** (`S2_Agent_OpenAI_Python.ipynb`) avant génération pour validation ?

---

[SEMAINE 1](https://app.notion.com/p/SEMAINE-1-29496ad943c180749f5ec1b7203d441b?pvs=21)

[Semaine 2 — Agents IA : Fondations & API (1h/jour)](https://app.notion.com/p/Semaine-2-Agents-IA-Fondations-API-1h-jour-28e96ad943c18091892fe572b8638907?pvs=21)

[Semaine x - jour 1](https://app.notion.com/p/Semaine-x-jour-1-28d96ad943c180fe964cd2ce07079a41?pvs=21)

[Semaine 4](https://app.notion.com/p/Semaine-4-2a496ad943c1804ab518cdca3ea2705f?pvs=21)

[Details version 1](https://app.notion.com/p/Details-version-1-37d96ad943c1803ba9b9ecfe8ba2aa68?pvs=21)

[Nouvelle forme de formations](https://app.notion.com/p/Nouvelle-forme-de-formations-38796ad943c180c89685cf651f4b4225?pvs=21)

[Semaine 3](https://app.notion.com/p/Semaine-3-38796ad943c18022a5c0c59b0b53a80e?pvs=21)

[Lectures](https://app.notion.com/p/Lectures-28796ad943c18016b763cd8322103a24?pvs=21)