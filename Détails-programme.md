# Détails

Voici un rappel complet du programme d'apprentissage de votre formation d'expert en ingénierie de l'IA, structuré sur **8 semaines**  :

---

### 📚 Semaine 1 — Bases & Consolidation

**Objectif :** Poser des fondations solides en ingénierie de prompt et modélisation.

* **Sujets abordés :** Types de modèles (GPT, BERT, T5, autoregressifs vs encodeurs-décodeurs), prompt engineering fondamental, techniques avancées (Few-Shot, Chain-of-Thought, prompt patterns), et session de consolidation.



---

### 🛠️ Semaine 2 — Agents IA : Fondations & API

**Objectif :** Maîtriser les briques de base de la conception d'agents (Function Calling, gestion de session).

* **Jour 1 :** Vue d’ensemble agents vs LLM (architectures, cas d'usage, limites).


* **Jour 2 :** OpenAI Function Calling et Responses API (schémas JSON, définitions de fonctions).


* **Jour 3 :** Implémentation d'un agent simple avec mock local.


* **Jour 4 :** Gestion du dialogue et de l'état de session (maintien du contexte à court terme).


* **Jour 5 :** Connexion d'outils externes (appels HTTP, mock de moteur de recherche).


* **Jour 6 :** Tests et défenses (assainissement des entrées, politiques de refus).


* **Jour 7 :** Revue de code, nettoyage et refactorisation du prototype.



---

### 🌐 Semaine 3 — Multi-agent & Protocole MCP

**Objectif :** Comprendre le protocole MCP d'Anthropic et implémenter des architectures d'échanges multi-agents.

* **Jour 1 :** Concepts multi-agents et définition des rôles (Analyst, Planner, Executor, Arbiter).


* **Jour 2 :** Introduction au Model Context Protocol (MCP), objectifs et format des messages.


* **Jour 3 :** Implémentation d'un échange MCP minimal (via HTTP ou bus de messages simulé).


* **Jour 4 :** Patterns de coordination et négociation (vote, consensus, arbitrage).


* **Jour 5 :** Sécurité inter-agents (scopes d'accès, filtres et autorisations).


* **Jour 6 :** Analyse comparative simple (mesure de la latence, des itérations et de la robustesse).


* **Jour 7 :** Mini-projet : alignement de 2 agents coopérants (Retrieval $\rightarrow$ Plan $\rightarrow$ Execution) avec logs.



---

### 🧱 Semaine 4 — Frameworks d'Agents (Semaine actuelle)

**Objectif :** Passer d'un agent ad-hoc codé manuellement à un agent orchestré par des frameworks professionnels.

* **Jour 1 :** Pourquoi les frameworks existent et présentation des premiers composants (*validé*).


* **Jour 2 :** Développement complet de notre propre micro-framework d'agents (`mini_framework` de ~300 lignes) (*validé*).


* **Jour 3 :** Ajout d'un moteur de workflow graphique (`Graph`, `Node`, `Edge`, `State`) (*validé*).


* **Jour 4 :** Réimplémentation de notre projet sous **LangGraph** (*validé*).


* **Jour 5 :** Réimplémentation de notre projet sous l'**OpenAI Agents SDK** (*validé*).


* **Jour 6 :** Comparaison technique et pratique entre **CrewAI**, **Google ADK** et **AutoGen** (*prochaine étape*).


* **Jour 7 :** Refactorisation de notre micro-framework pour en faire un package de production complet.



---

### 🚀 Semaine 5 — Concevoir une architecture IA prête pour la production

**Question de la semaine :** *Comment transformer un prototype d'agent en un service fiable, sécurisé et scalable?* 

* **Jour 1 :** Architecturer un système IA moderne (conception de la stack : FastAPI, Redis, PostgreSQL, LLM).


* **Jour 2 :** Conception d'une API d'agents asynchrone (FastAPI, Server-Sent Events (SSE), WebSockets, quotas).


* **Jour 3 :** Stratégies de déploiement (Dockerisation, architectures serverless et environnements cloud managés).


* **Jour 4 :** Passage à l'échelle (workers, files d'attente, concepts Kubernetes et mise en cache).


* **Jour 5 :** Observabilité et monitoring (coût des tokens, latence, OpenTelemetry, LangSmith/Phoenix).


* **Jour 6 :** Sécurité avancée des agents (Prompt Injections directes/indirectes, Tool Abuse, Guardrails).


* **Jour 7 :** Revue d'architecture globale et soutenance des diagrammes système.



---

### 🔍 Semaine 6 — Le RAG comme outil d'un agent

**Question de la semaine :** *Comment permettre à un agent de raisonner sur des connaissances qu'il ne possède pas?* 

* **Jour 1 :** Place du RAG dans l'écosystème actuel et gestion des limites de fenêtres de contexte.


* **Jour 2 :** Exploration des Vector Stores et calcul des Embeddings (similarité cosinus, choix du modèle).


* **Jour 3 :** Construction du premier pipeline RAG complet et connecté à un LLM.


* **Jour 4 :** Optimisation du Retrieval (recherche hybride, reranking, compression de contexte).


* **Jour 5 :** Évaluation des performances d'un RAG (Recall, Precision, Faithfulness) et mini-framework d'évaluation.


* **Jour 6 :** Stratégies de réduction des coûts de tokens d'entrée et techniques de chunking avancé.


* **Jour 7 :** Intégration finale du RAG en tant qu'outil actionnable par notre agent du projet fil rouge.



---

### ⚙️ Semaine 7 — Workflow Engineering & Automatisation

**Question de la semaine :** *Quand faut-il coder et quand faut-il orchestrer?* 

* **Jour 1 :** Les types de workflows (synchrone, asynchrone, événementiel, Human-in-the-loop).


* **Jour 2 :** Prise en main de l'outil n8n (forces, limites et interconnexion).


* **Jour 3 :** Intégration d'un agent IA autonome au sein d'un workflow n8n (ex: Email $\rightarrow$ Agent $\rightarrow$ CRM).


* **Jour 4 :** Comparaison des orchestrateurs de tâches (n8n, Temporal, GitHub Actions, AWS Step Functions).


* **Jour 5 :** Patterns d'escalade et validation par l'humain (Human-in-the-loop).


* **Jour 6 :** Création d'un processus hybride intégrant l'automatisation, l'IA et l'intervention humaine.


* **Jour 7 :** Réalisation d'un projet métier complet (support client, relecture documentaire automatisée).



---

### 📈 Semaine 8 — Évaluation, optimisation et gouvernance

**Question de la semaine :** *Comment garantir qu'un système IA reste fiable dans le temps?* 

* **Jour 1 :** Création de jeux de tests automatisés et benchmarks d'évaluation comportementale des agents.


* **Jour 2 :** Optimisation des temps de réponse (parallélisme, asynchronisme et mise en cache).


* **Jour 3 :** Arbitrages qualité/coûts et gestion des budgets de jetons en production.


* **Jour 4 :** Gouvernance, conformité légale (RGPD) et traçabilité des décisions agentiques.


* **Jour 5 :** Études de cas stratégiques : quand choisir le développement sur-mesure ou des plateformes tierces.


* **Jour 6 :** Préparation du dossier de projet professionnel (Architecture Decision Records (ADR), diagrammes).


* **Jour 7 :** Soutenance technique finale et présentation du projet fil rouge `ai-agent-lab/`.



---

N'hésitez pas à me dire si vous souhaitez que nous passions dès à présent à la rédaction du contenu pour le **Jour 6 de la Semaine 4**, qui comparera en profondeur **CrewAI**, **Google ADK** et **AutoGen**.