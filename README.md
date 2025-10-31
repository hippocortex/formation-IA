# 🧠 Formation – Évolution vers l’IA appliquée

## 📘 Présentation

Ce dépôt regroupe mes travaux, notebooks et ressources dans le cadre de ma **formation personnelle en Intelligence Artificielle appliquée**, avec un focus sur :
- le **développement d’agents IA** (OpenAI, LangChain, MCP),
- le **NLP (Natural Language Processing)**,
- le **Machine Learning** (concepts, implémentations),
- et les **architectures modernes IA / RAG**.

L’objectif est d’évoluer professionnellement vers un rôle de **développeur backend spécialisé IA** ou **architecte solutions IA**.

---

## 🗂 Structure du dépôt

formation-ia/
│
├── semaine_1/
│ ├── S1_J1_Types_de_modeles_LLM.ipynb
│ ├── S1_J2_Prompt_Engineering.ipynb
│ └── notes.md
│
├── semaine_2/
│ ├── S2_Agent_OpenAI_Python.ipynb
│ ├── S2_Agent_OpenAI_LangChain.ipynb
│ └── notes.md
│
├── semaine_3/
│ ├── S3_Function_Calling_RAG.ipynb
│ └── notes.md
│
├── semaine_4/
│ ├── S4_MultiAgent_MCP_Python.ipynb
│ ├── S4_MultiAgent_MCP_LangChain.ipynb
│ └── notes.md
│
├── utils/
│ ├── requirements.txt
│ ├── config_example.env
│ └── helpers.py
│
└── README.md


---

## 🚀 Installation

### 1️⃣ Cloner le dépôt
```bash
git clone https://github.com/<ton-pseudo>/formation-ia.git
cd formation-ia
```
### 2️⃣ Créer un environnement virtuel
```
python -m venv .venv
source .venv/bin/activate  # sous Windows : .venv\Scripts\activate
```

### 3️⃣ Installer les dépendances
```
pip install -r utils/requirements.txt
```

### 4️⃣ Configurer ta clé OpenAI (mode API)

Copie le fichier .env :
```
cp utils/config_example.env .env
```
💡 Utilisation dans un notebook Jupyter

Dans n’importe quel notebook de ta formation, tu pourras écrire :
```
from load_env import load_environment
env = load_environment()

import openai
openai.api_key = env["OPENAI_API_KEY"]
```

