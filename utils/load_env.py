"""
load_env.py
==================
Ce script charge les variables d'environnement depuis un fichier `.env`
et les rend accessibles dans les notebooks Jupyter et scripts Python.

Usage :
--------
1. Copie ce fichier à la racine de ton dépôt.
2. Crée un fichier `.env` à partir du modèle `.env.example`.
3. Dans ton notebook, exécute :

   from load_env import load_environment
   env = load_environment()

   # Exemple d'accès à la clé API :
   print(env["OPENAI_API_KEY"])

Ce script vérifie également la présence des variables critiques (comme OPENAI_API_KEY).
"""

import os
from dotenv import load_dotenv
from pathlib import Path


def load_environment(env_file: str = ".env"):
    """
    Charge les variables d'environnement depuis un fichier `.env`.
    Si le fichier n'existe pas, affiche un avertissement.

    Retourne :
        dict : les variables d'environnement chargées
    """
    env_path = Path(env_file)
    if not env_path.exists():
        raise FileNotFoundError(
            f"⚠️ Le fichier {env_file} est introuvable.\n"
            "Crée-le à partir du modèle `.env.example`."
        )

    # Chargement du fichier .env
    load_dotenv(dotenv_path=env_path)

    # Lecture des variables d'environnement essentielles
    env = {
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "OPENAI_MODEL": os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
        "OPENAI_BASE_URL": os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1"),
        "EXECUTION_MODE": os.getenv("EXECUTION_MODE", "real"),
    }

    # Vérification de la présence de la clé API
    if not env["OPENAI_API_KEY"]:
        print(
            "⚠️  Avertissement : la variable OPENAI_API_KEY n'est pas définie.\n"
            "    Pense à créer ton fichier `.env` à partir de `.env.example`."
        )

    print("✅ Environnement chargé avec succès.")
    return env


# Si le script est exécuté directement
if __name__ == "__main__":
    env = load_environment()
    print(env)
