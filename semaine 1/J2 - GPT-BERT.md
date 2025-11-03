Présentation Technique : Au Cœur des Mécanismes d'Attention – BERT vs. GPT

1.0 Introduction : L'Attention, Moteur des Transformers

Le mécanisme d'attention est la pierre angulaire du succès des architectures Transformer. Son importance stratégique réside dans sa capacité à dépasser les limites des modèles séquentiels précédents, en permettant une compréhension contextuelle avancée du langage. Plutôt que de traiter le texte mot par mot de manière linéaire, l'attention permet au modèle de peser l'importance de chaque mot par rapport à tous les autres, créant ainsi une représentation riche et dynamique des relations sémantiques.

L'objectif de cette présentation est de démystifier et de comparer les deux principaux types de flux d'attention qui animent les modèles les plus connus : le flux bidirectionnel de BERT et le flux causal de GPT. Nous explorerons également le calcul fondamental des vecteurs qui les sous-tendent : Query, Key et Value.

Cette distinction fondamentale entre les modèles prend racine dans leur architecture même, nous amenant à distinguer les modèles basés sur l'encodeur de ceux basés sur le décodeur.

2.0 Fondements Architecturaux : Encodeur (BERT) vs. Décodeur (GPT)

La structure architecturale d'un Transformer dicte sa fonction principale. Selon qu'un modèle utilise uniquement la partie encodeur, uniquement la partie décodeur, ou les deux, il sera spécialisé soit dans la compréhension de texte, soit dans la génération de texte.

┌────────────────────────────────────────────┐
│                TRANSFORMER                 │
└────────────────────────────────────────────┘
                  ↑           ↑
   Encoder (BERT, T5)      Decoder (GPT, T5)


Comme l'illustre ce schéma, BERT n'utilise que la partie "Encoder", GPT n'utilise que la partie "Decoder", et des modèles comme T5 utilisent les deux. Cette différence architecturale se traduit par deux approches radicalement différentes du traitement du langage.

* BERT : Le Lecteur Analyste BERT lit tout le texte d'un coup, en regardant à la fois en avant et en arrière, pour en comprendre le sens global. C'est comme un analyste qui étudie un document dans son intégralité, en faisant des allers-retours pour saisir toutes les nuances et les relations entre les mots.
* GPT : L'Écrivain Attentif GPT lit ce qui a été écrit jusqu'à présent pour comprendre le contexte, puis continue le récit. Il progresse de manière séquentielle, en se basant uniquement sur le passé pour prédire le futur, tel un écrivain qui relit son dernier paragraphe avant d'écrire le suivant.

Cette compréhension n'est pas superficielle. En empilant de multiples couches d'attention, GPT parvient à construire des représentations contextuelles si riches qu'on peut les voir comme un "encodeur interne" qui se forme progressivement, lui permettant de saisir des relations complexes à longue distance dans le texte déjà généré. Une nuance cruciale doit donc être apportée pour GPT : bien qu'étant "Decoder-only", il intègre la compréhension dans son mécanisme de génération. Le prompt est traité comme un contexte interne, que le modèle analyse avant de produire une suite logique. En résumé, GPT "comprend en générant".

Plongeons maintenant dans le calcul mathématique qui rend cette attention si puissante et flexible.

3.0 Le Mécanisme d'Auto-Attention : Le Calcul des Vecteurs Query, Key et Value (QKV)

Pour évaluer l'importance des mots les uns par rapport aux autres, la couche d'auto-attention crée trois représentations vectorielles distinctes pour chaque token d'entrée : Query (Q), Key (K) et Value (V). Ce mécanisme est le cœur du calcul de l'attention et permet au modèle de mesurer la pertinence entre les différents mots d'une séquence.

Le processus de calcul se déroule en deux étapes clés :

1. Embedding initial : Chaque mot est d'abord transformé en un vecteur numérique dense, appelé embedding.
2. Projection linéaire : Cet embedding est ensuite multiplié par trois matrices de poids distinctes et apprises durant l'entraînement (WQ, WK, WV) pour obtenir les trois vecteurs Q, K et V.

Les formules mathématiques correspondantes, pour une matrice d'embeddings X, sont les suivantes :

* Query (Q) = X * WQ
* Key (K) = X * WK
* Value (V) = X * WV

La signification intuitive de chaque vecteur peut être synthétisée ainsi :

* Query : Ce que le mot "demande" aux autres mots.
* Key : Ce que le mot "offre" pour être comparé.
* Value : L'information contenue à transmettre si la connexion est forte.

C'est la manière dont les modèles autorisent ou restreignent les interactions entre ces vecteurs qui définit leur spécialisation, comme nous allons le voir dans l'analyse des flux d'attention de GPT et BERT.

4.0 Analyse Comparée des Flux d'Attention

La manière dont un modèle gère les interactions entre les vecteurs Query, Key et Value est ce qui le spécialise pour la compréhension ou la génération. Nous allons maintenant analyser en détail comment les flux d'attention de GPT et de BERT diffèrent fondamentalement.

4.2 L'Attention Causale (ou Unidirectionnelle) de GPT

L'attention causale est un mécanisme où chaque mot ne peut "regarder" que les mots qui le précèdent dans la séquence. Cela empêche le modèle de "voir le futur", le forçant à générer du texte de manière auto-régressive, un mot à la fois, en se basant uniquement sur le contexte passé.

Prompt : "Le chat dort"
[Le] → [chat] → [dort] → [sur] → [le] → [canapé]


Analysons l'exemple "Le chat dort sur le canapé" avec une matrice d'attention simplifiée pour illustrer ce fonctionnement. Dans la matrice ci-dessous, chaque ligne (t) représente le token cible qui calcule son attention, et chaque colonne (s) représente le token source qu'il regarde.

Token cible (t)	s=1 (Le)	s=2 (chat)	s=3 (dort)	s=4 (sur)	s=5 (le)	s=6 (canapé)
t=1 (Le)	1.00	0.00	0.00	0.00	0.00	0.00
t=2 (chat)	0.60	0.40	0.00	0.00	0.00	0.00
t=3 (dort)	0.20	0.50	0.30	0.00	0.00	0.00
t=4 (sur)	0.10	0.30	0.40	0.20	0.00	0.00
t=5 (le)	0.05	0.15	0.25	0.35	0.20	0.00
t=6 (canapé)	0.02	0.08	0.05	0.25	0.50	0.10

Interprétation détaillée :

* dort (t=3) accorde un poids élevé (0.50) à chat, car le verbe a besoin de savoir qui est le sujet de l'action.
* le (t=5) est fortement conditionné par la préposition sur (0.35), qui crée une attente structurelle pour un article suivi d'un nom.
* canapé (t=6), pour être généré, regarde principalement l'article qui le précède (le, avec un poids de 0.50) et la préposition sur (0.25). Les tokens plus anciens comme le sujet (chat) ont un poids plus faible mais contribuent à la cohérence globale.

Cette approche séquentielle, où chaque nouveau mot est prédit à partir de la combinaison pondérée du passé, est idéale pour les tâches de génération de texte (next-token prediction).

4.3 L'Attention Bidirectionnelle de BERT

À l'inverse, l'attention bidirectionnelle permet à chaque mot de "regarder" tous les autres mots de la séquence, qu'ils soient placés avant ou après. Cette vision à 360° fournit un contexte global et complet.

Phrase : "Le chat dort."
[Le] ←→ [chat] ←→ [dort]


Reprenons le même exemple, "Le chat dort sur le canapé", avec une matrice d'attention typique de BERT. Dans la matrice ci-dessous, chaque ligne (t) représente le token cible qui calcule son attention, et chaque colonne (s) représente le token source qu'il regarde.

Token cible (t)	s=1 (Le)	s=2 (chat)	s=3 (dort)	s=4 (sur)	s=5 (le)	s=6 (canapé)
t=1 (Le)	0.25	0.30	0.10	0.10	0.15	0.10
t=2 (chat)	0.20	0.25	0.20	0.10	0.15	0.10
t=3 (dort)	0.10	0.25	0.30	0.15	0.10	0.10
t=4 (sur)	0.10	0.10	0.20	0.35	0.15	0.10
t=5 (le)	0.10	0.10	0.10	0.25	0.35	0.10
t=6 (canapé)	0.05	0.05	0.05	0.20	0.30	0.35

Interprétation détaillée :

* Différence clé : Le premier token, Le (t=1), peut désormais accorder une forte attention au mot chat (0.30) qui le suit, ce qui est impossible pour GPT. Il comprend son rôle de déterminant en fonction du nom qui vient après. Cette capacité à "regarder vers l'avant" est ce qui permet à BERT de désambiguïser des phrases complexes où le sens d'un mot dépend entièrement de ce qui suit, une tâche impossible pour une architecture purement causale.
* dort (t=3) se focalise logiquement sur le sujet chat (0.25) pour identifier qui réalise l'action.
* canapé (t=6) se base fortement sur l'article le (0.30) et la préposition sur (0.20) qui le précèdent, mais sa représentation est enrichie par les interactions avec tous les autres mots de la phrase.

Cette vision contextuelle globale rend BERT exceptionnellement performant pour les tâches de compréhension. C'est précisément cette vision à 360° qui est requise pour sa tâche de pré-entraînement principale, le Masked Language Modeling (MLM), où le modèle doit deviner un mot manquant en utilisant à la fois le contexte qui le précède et celui qui le suit. Une synthèse finale permettra de consolider ces différences fondamentales et de les lier à des cas d'usage concrets.

5.0 Synthèse et Cas d'Usage

Nous avons vu que l'architecture et le type d'attention déterminent la spécialisation d'un modèle. Pour les ingénieurs et développeurs, choisir le bon outil pour la bonne tâche est fondamental. Cette section récapitule les différences clés entre BERT et GPT et leurs applications respectives.

Le tableau suivant oppose directement les deux modèles sur leurs caractéristiques fondamentales.

Caractéristique	BERT (Encoder)	GPT (Decoder-only)
Type d'attention	Bidirectionnelle	Unidirectionnelle (causale)
Rôle principal	Compréhension du texte	Génération de texte
Flux de données	Tous les tokens se voient mutuellement	Chaque token ne voit que les précédents
Exemples d'usage	Analyse de texte, recherche, QA	Chatbot, rédaction, complétion de code
Exemple de tâche	Remplir un mot manquant	Prédire le mot suivant

Les forces et limites de chaque architecture découlent directement de ces choix de conception :

* GPT :
  * Forces : Très performant pour générer du texte fluide.
  * Limites : Mauvaise compréhension bidirectionnelle.
* BERT :
  * Forces : Excellente compréhension contextuelle.
  * Limites : Ne peut pas générer de texte.

Passons maintenant aux points clés à retenir de cette présentation.

6.0 Conclusion : Points Clés à Retenir

Pour conclure cette formation, voici les trois enseignements fondamentaux à retenir sur les mécanismes d'attention dans les architectures Transformer.

1. L'architecture dicte la fonction. La structure interne d'un modèle est son destin. Les modèles Encoder-only comme BERT sont conçus pour la compréhension de texte, tandis que les modèles Decoder-only comme GPT excellent dans la génération.
2. Le flux d'attention est la clé. La différence fondamentale réside dans la manière dont l'information circule. L'attention bidirectionnelle de BERT lui offre un contexte global, parfait pour l'analyse. L'attention causale (unidirectionnelle) de GPT lui fournit un contexte progressif, idéal pour la prédiction séquentielle.
3. QKV est le mécanisme universel. Quel que soit le modèle, le calcul de l'attention repose sur le même principe fondamental : la projection des embeddings de mots en trois vecteurs distincts – Query, Key et Value. C'est ce mécanisme qui permet de pondérer dynamiquement les relations entre les mots.

En appliquant ces connaissances, vous serez mieux armés pour choisir, concevoir et déboguer vos propres pipelines d'IA. Pour simplifier à l'extrême, gardez cette note en tête : GPT écrit, BERT comprend.
