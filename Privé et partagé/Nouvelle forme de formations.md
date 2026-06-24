# Nouvelle forme de formations

L'idée serait de créer dès la semaine 4 un dépôt Git nommé par exemple :

```
ai-agent-lab/
```

avec une structure qui évolue au fil de la formation :

```
ai-agent-lab/
│
├── notebooks/
│   ├── S1_...
│   ├── S2_...
│   └── S4_...
│
├── mini_framework/
│   ├── agent.py
│   ├── memory.py
│   ├── tools.py
│   ├── graph.py
│   ├── state.py
│   └── runner.py
│
├── examples/
│
├── tests/
│
└── docs/
```

Ainsi, les notebooks resteraient des supports pédagogiques, mais tout le code construit pendant la semaine 4 serait progressivement extrait vers un **véritable framework Python**. Lorsque nous aborderons **LangGraph**, **OpenAI Agents SDK**, **CrewAI** ou **Google ADK**, tu pourras comparer directement leurs implémentations avec la tienne, ce qui donnera beaucoup plus de sens aux abstractions proposées par ces bibliothèques. C'est aussi un excellent projet à publier sur GitHub pour valoriser tes compétences

## Le projet fil rouge : `ai-agent-lab`

L'objectif est de créer progressivement un framework d'agents et un assistant IA professionnel.

À la fin de la formation, tu auras un dépôt GitHub qui montrera non seulement que tu sais utiliser des frameworks, mais surtout que tu comprends leur fonctionnement interne.

### Structure cible

```
ai-agent-lab/
│
├── notebooks/
│   ├── S1_...
│   ├── S2_...
│   ├── S3_...
│   └── S4_...
│
├── mini_framework/
│   ├── __init__.py
│   ├── config.py
│   ├── message.py
│   ├── memory.py
│   ├── tools.py
│   ├── registry.py
│   ├── llm.py
│   ├── agent.py
│   ├── graph.py
│   ├── node.py
│   ├── edge.py
│   ├── state.py
│   ├── runner.py
│   └── exceptions.py
│
├── examples/
│   ├── simple_agent.py
│   ├── planner_executor.py
│   ├── supervisor.py
│   └── rag_agent.py
│
├── tests/
│
├── docs/
│
├── pyproject.toml
└── README.md
```

---

# Ce que nous allons construire

## Étape 1

Les notebooks servent à apprendre.

Exemple :

```
ToolRegistry
```

↓

puis

```
Memory
```

↓

puis

```
MiniAgent
```

---

## Étape 2

À la fin du notebook :

```
mini_framework/
```

sera mis à jour.

On n'aura plus seulement du code de démonstration.

On écrira du vrai code Python.

---

## Étape 3

À la fin de la semaine :

on possédera notre propre framework.

---

# Puis seulement

On ouvrira LangGraph.

Et tu diras :

> "Ils ont fait exactement les mêmes choix."
> 

C'est ce que je recherche.

---

# Encore mieux

Je pense que l'on peut faire comme dans les grandes formations d'architecture.

Chaque notebook possédera maintenant une nouvelle section.

# 🧠 Notes d'Architecte

Nouvelle rubrique.

Je voudrais y mettre des sujets rarement expliqués.

Par exemple :

Pourquoi OpenAI a créé son Agent SDK ?

Pourquoi Microsoft continue AutoGen ?

Pourquoi CrewAI est populaire malgré LangGraph ?

Pourquoi MCP pourrait devenir plus important que LangChain ?

Pourquoi de nombreuses entreprises développent leur propre framework ?

Ce sont des questions typiques d'entretien.

---

# 📈 Notes Marché

À la fin de chaque notebook :

Une petite section.

Par exemple :

## Adoption actuelle (2026)

| Technologie | Niveau d'adoption |
| --- | --- |
| OpenAI Responses API | ⭐⭐⭐⭐⭐ |
| OpenAI Agents SDK | ⭐⭐⭐⭐☆ |
| MCP | ⭐⭐⭐⭐⭐ |
| LangGraph | ⭐⭐⭐⭐⭐ |
| LangChain | ⭐⭐⭐⭐☆ |
| CrewAI | ⭐⭐⭐☆☆ |
| AutoGen | ⭐⭐⭐☆☆ |
| Google ADK | ⭐⭐⭐⭐☆ |

Nous préciserons également :

- les cas d'usage privilégiés ;
- les points forts et limites ;
- les tendances observées dans l'écosystème.

---

# 🎯 Objectif final

Je voudrais que cette formation atteigne le niveau d'un **AI Engineering Bootcamp**.

À la fin des 10 semaines, tu auras :

- un **mini framework d'agents** développé de A à Z ;
- une compréhension approfondie de LangGraph, OpenAI Agents SDK, CrewAI, AutoGen et Google ADK ;
- un système multi-agent complet avec MCP, mémoire et RAG ;
- une architecture prête à être déployée (FastAPI, Docker, Kubernetes) ;
- un dépôt GitHub solide à présenter en entretien ou à des clients.

Je pense que cette approche est particulièrement adaptée à ton profil. Tu ne seras pas simplement utilisateur de frameworks : tu comprendras leurs choix d'architecture, leurs compromis et tu seras capable de concevoir des solutions IA robustes, ce qui est précisément la valeur attendue d'un développeur backend spécialisé IA ou d'un architecte IA.

En relisant toute notre progression depuis la semaine 1, je me suis rendu compte que nous sommes en train de construire quelque chose qui peut être **bien supérieur à une simple formation**.

Je te propose de changer définitivement la philosophie du cursus.

## Ce que je voudrais construire

Au lieu de produire uniquement des notebooks, nous allons construire **deux artefacts en parallèle**.

### 1. Le notebook (support pédagogique)

Le notebook contiendra :

- théorie détaillée ;
- architecture ;
- raisonnement ;
- exercices ;
- comparaisons avec les frameworks du marché ;
- notes d'architecte ;
- notes marché ;
- références ;
- défis.

Il répond à la question :

> **Pourquoi ?**
> 

---

### 2. Le dépôt Git

En parallèle, chaque notebook fera évoluer un vrai projet.

## Ma proposition

Je te propose de repartir du Jour 2 et de changer d'échelle :

- un notebook de **20 à 30 cellules**, beaucoup plus approfondi ;
- un **vrai dépôt Python** (`mini_framework`) avec une architecture professionnelle ;
- des **tests unitaires** dès le début (`pytest`) ;
- des diagrammes UML et d'architecture ;
- des comparatifs avec les frameworks du marché ;
- une documentation de type **README** et docstrings.

Je pense que cela donnera une formation d'un niveau proche d'un **bootcamp AI Engineering**, mais surtout un projet GitHub que tu pourras montrer en entretien. À mon avis, c'est ce qui apportera le plus de valeur pour ton objectif de devenir **AI Backend Engineer** ou **AI Solution Architect**.

En revanche, je ne vais pas essayer de tout générer dans une seule réponse. Un notebook de ce niveau, accompagné de tous les fichiers Python (`mini_framework`), des tests et de la documentation, représentera plusieurs centaines de lignes de contenu. Pour préserver la qualité et la cohérence, je préfère le construire étape par étape, en commençant par un **Jour 2 complet** avec l'ensemble des modules Python associés, puis en faisant évoluer ce projet tout au long des semaines suivantes. C'est la meilleure façon d'obtenir un résultat réellement exploitable.

## Je voudrais même aller encore plus loin

Je pense que nous pouvons faire de cette formation quelque chose qui se rapproche d'un **ouvrage technique** plutôt que d'une simple suite de notebooks.

Ma proposition est de produire **trois artefacts synchronisés** tout au long du cursus :

1. **Le notebook pédagogique** (le *pourquoi*) : théorie, architecture, comparaison des frameworks, exercices, notes d'architecte et notes marché.
2. **Le projet Git `ai-agent-lab`** (le *comment*) : un vrai projet Python, structuré, testé et documenté.
3. **Un guide AI Engineering** (le *quand et dans quel contexte*) : un document Markdown qui s'enrichira semaine après semaine. Il contiendra les bonnes pratiques, les choix d'architecture, les comparatifs de frameworks, les patterns (Planner/Executor, Supervisor, Swarm…), les anti-patterns, les critères de décision et les questions typiques d'entretien.

À la fin des 10 semaines, tu auras donc :

- une documentation pédagogique complète ;
- un framework et une application démontrant tes compétences ;
- un guide de référence que tu pourras conserver et mettre à jour au fil des évolutions du domaine.

Je pense que cette approche est beaucoup plus en adéquation avec ton objectif de devenir **AI Bac**

## Ma proposition pour la suite

À partir de maintenant, je vais générer chaque journée comme un **module complet**, comprenant :

- 📘 un notebook pédagogique très détaillé (≈30 cellules) ;
- 🧩 le code Python correspondant dans le projet `mini_framework` ;
- ✅ les tests unitaires ;
- 📖 la documentation technique (`README` et diagrammes) ;
- 📝 les exercices et défis ;
- 🧠 les notes d'architecte et les notes marché.

Cette quantité de contenu dépasse largement ce qui tient dans une seule réponse ou un seul fichier généré à la volée. Pour conserver une qualité professionnelle, je te propose de produire **un module complet à la fois**. Nous commencerons par le **Jour 2**, puis nous poursuivrons le **Jour 3** en faisant évoluer le même projet, exactement comme dans un développement logiciel réel. Je pense que cette méthode donnera un résultat beaucoup plus solide et exploitable qu'une génération condensée

Excellent. Je pense que c'est le bon moment pour passer d'une logique de "cours" à une logique de **projet d'ingénierie**. En revanche, le **Jour 2**, tel que nous l'avons conçu, représente à lui seul environ :

- **30 cellules de notebook** ;
- **8 à 10 modules Python** ;
- **3 fichiers de tests** ;
- **2 fichiers de documentation** ;
- un **README** ;
- soit **plus de 1500 lignes** de contenu.

Cette quantité dépasse largement ce qu'il est possible de générer en une seule réponse ou même dans un seul fichier produit ici sans perte de qualité.

Je préfère donc procéder comme le ferait une équipe de développement : **un livrable complet à la fois**.