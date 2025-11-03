L'Algorithme Conflict-Based Search (CBS) : Expliqué Simplement

Le Conflict-Based Search (CBS) est une méthode intelligente pour résoudre le problème complexe de la planification de chemins pour plusieurs agents (robots, personnages de jeu, etc.) sans qu'ils se heurtent les uns aux autres.

1. Le Problème : Le Casse-tête du Labyrinthe Multi-Agents

L'algorithme CBS a été conçu pour résoudre un problème fondamental connu sous le nom de Multi-Agent Path Finding (MAPF). Imaginez plusieurs robots dans un entrepôt encombré, chacun devant atteindre une destination différente le plus rapidement possible, sans jamais se bousculer. C'est exactement le défi que le MAPF modélise.

Le problème repose sur un ensemble d'objectifs et de contraintes très clairs :

* Contrainte 1 : Collision de sommet (Vertex Conflict) Deux agents ne peuvent pas occuper la même case (ou le même "sommet") au même instant.
* Contrainte 2 : Collision d'arête (Edge Conflict) Deux agents ne peuvent pas se croiser en empruntant le même chemin (ou la même "arête") en sens inverse au même moment.
* Objectif commun Le but est de trouver une solution qui minimise un coût total. Le plus souvent, il s'agit de la somme des distances (ou du temps de parcours) de tous les agents, un critère appelé sum-of-costs.

Face à cette complexité, l'astuce de CBS est de refuser de tout résoudre en même temps. Il parie sur une approche de "division pour mieux régner".

2. L'Idée Maîtresse de CBS : Diviser pour Mieux Régner

Le principe fondamental de CBS est de décomposer le problème global en deux niveaux de recherche distincts, chacun avec une mission spécifique. Cette séparation est la clé de son efficacité.

Recherche de Bas Niveau (Les Planificateurs Individuels)	Recherche de Haut Niveau (Le Gestionnaire de Conflits)
Mission : Trouver le chemin optimal pour un seul agent, en ignorant les autres mais en respectant un ensemble de règles (contraintes) qui lui sont imposées.	Mission : Superviser l'ensemble, détecter les collisions entre les chemins individuels, et ajouter des règles pour forcer les agents à se coordonner.

Grâce à cette séparation, CBS évite d'explorer l'immense espace de recherche combiné de tous les agents. Il ne se concentre sur les interactions que lorsqu'un conflit se produit, ce qui le rend bien plus efficace.

3. La Recherche de Bas Niveau : L'Expert Solitaire

La recherche de bas niveau a une mission simple et ciblée : calculer le meilleur chemin possible pour un seul agent, comme si celui-ci était seul au monde, tout en obéissant à des ordres précis.

Son processus se déroule comme suit :

1. Entrée : Il reçoit la position de départ et d'arrivée d'un agent unique, ainsi qu'un ensemble de contraintes spécifiques. Une contrainte est un ordre simple, par exemple :
2. Tâche : Il utilise un algorithme de recherche de chemin standard, comme A*, pour trouver le chemin le plus court qui respecte absolument toutes les contraintes imposées.
3. Sortie : Il retourne ce chemin optimal unique. S'il n'en trouve aucun qui respecte les règles, il signale un échec.

Cette partie de la tâche est relativement simple car elle ne concerne qu'un agent à la fois. La véritable "magie" de CBS réside dans la manière dont le haut niveau coordonne ces experts solitaires.

4. La Recherche de Haut Niveau : Le Chef d'Orchestre

Le haut niveau agit comme un chef d'orchestre méticuleux. Il ne joue d'aucun instrument lui-même (il ne calcule pas de chemin), mais écoute la symphonie des chemins individuels. Dès qu'il entend une fausse note (un conflit), il arrête tout, donne une nouvelle instruction (une contrainte) à un ou deux musiciens, et leur demande de rejouer leur partition.

4.1. L'Outil Principal : L'Arbre de Contraintes (Constraint Tree)

Le haut niveau organise sa recherche à l'aide d'un Arbre de Contraintes (en anglais, Constraint Tree ou CT). On peut voir cet arbre comme un plan de travail où chaque "nœud" représente une tentative de solution globale.

Un nœud de cet arbre contient trois informations clés :

* Un ensemble de contraintes : Les règles qui s'appliquent aux agents à ce stade de la recherche.
* Une solution candidate : Un ensemble de chemins (un par agent) calculés par le bas niveau en respectant ces contraintes.
* Un coût total : La somme des coûts de tous les chemins de la solution candidate.

4.2. Le Processus : Détection et Résolution des Conflits

Le haut niveau suit un processus méthodique pour trouver une solution sans conflit et optimale.

1. Initialisation : L'algorithme commence avec un nœud Racine dans l'arbre, qui n'a aucune contrainte (contraintes = ∅). Il demande alors au bas niveau de trouver le chemin optimal pour chaque agent, sans aucune restriction.
2. Sélection : Le haut niveau choisit le nœud le plus prometteur à explorer. C'est toujours celui qui a le coût total le plus faible.
3. Validation : Il analyse la solution du nœud sélectionné pour voir si elle est "valide", c'est-à-dire si des agents se rentrent dedans. Si aucun conflit n'est trouvé, c'est la solution optimale ! L'algorithme s'arrête et retourne cette solution.
4. Détection : Si la solution n'est pas valide, il identifie le premier conflit. Par exemple : (agent_1, agent_2, case_V, temps_T), ce qui signifie que les agents 1 et 2 se trouvent sur la même case V au même instant T.
5. Résolution (la bifurcation) : C'est l'étape cruciale. Pour résoudre le conflit, le nœud actuel est "divisé" en deux nouveaux nœuds enfants, créant une branche dans l'arbre :
  * Enfant 1 : Hérite de toutes les contraintes de son parent, PLUS la nouvelle contrainte (agent_1, case_V, temps_T). On demande à l'agent 1 d'éviter cette position à ce moment précis.
  * Enfant 2 : Hérite de toutes les contraintes de son parent, PLUS la nouvelle contrainte (agent_2, case_V, temps_T). On demande cette fois à l'agent 2 de faire l'effort.
6. Cette bifurcation est le cœur de la garantie d'optimalité de CBS. En explorant systématiquement les deux seules issues possibles pour résoudre le conflit (soit l'agent 1 cède le passage, soit l'agent 2 le fait), l'algorithme s'assure de ne jamais écarter prématurément la véritable solution la moins coûteuse.
7. Mise à jour : Pour chaque enfant, le haut niveau redemande au bas niveau de recalculer le chemin, mais uniquement pour l'agent concerné par la nouvelle contrainte. Les chemins des autres agents restent inchangés. Le coût total du nœud est mis à jour.
8. Répétition : Les nouveaux nœuds enfants sont ajoutés à la liste des nœuds à explorer, et le processus recommence à l'étape 2.

On peut donc voir CBS comme deux niveaux de recherche optimale imbriqués : une recherche A* au bas niveau pour trouver le meilleur chemin individuel respectant les règles, et une recherche de type "Meilleur d'abord" au haut niveau pour trouver la meilleure combinaison de chemins sans conflit.

4.3. Exemple Concret : Deux Agents, un Conflit

Imaginons deux souris (agents) cherchant chacune leur fromage (destination) sur une grille.

1. Racine : Dans le nœud racine (sans contrainte), le bas niveau calcule les chemins les plus courts pour chaque souris. Le haut niveau valide cette solution et détecte un conflit : les deux souris arrivent sur la case C au temps t=2.
2. Bifurcation : Le nœud racine est divisé pour résoudre ce conflit.
  * Le Nœud A est créé avec la contrainte : (souris_1, C, 2).
  * Le Nœud B est créé avec la contrainte : (souris_2, C, 2).
3. Replanification :
  * Dans le Nœud A, on demande au bas niveau de trouver un nouveau chemin pour la souris_1 qui évite la case C au temps t=2. La souris pourrait, par exemple, attendre un tour, ce qui augmente le coût de son chemin et donc le coût total du Nœud A.
  * Dans le Nœud B, c'est la souris_2 qui doit recalculer son chemin pour éviter la collision.
4. Solution : L'algorithme explore ensuite le nœud qui a le nouveau coût total le plus faible (disons, le Nœud A). Il valide les chemins de ce nœud, ne trouve plus aucun conflit, et retourne cette solution comme étant la meilleure possible.

5. L'Efficacité de CBS : Points Forts et Faiblesses

L'élégance et l'efficacité de CBS proviennent d'un principe simple : contrairement aux approches qui explorent toutes les combinaisons de mouvements possibles, la complexité de CBS dépend principalement du nombre de conflits à résoudre, et non de manière exponentielle du nombre d'agents.

Cependant, son efficacité varie selon la nature du problème.

✅ Quand CBS Brille	⚠️ Quand CBS Peine
CBS est très performant lorsque les conflits sont rares ou localisés. Il excelle dans les environnements avec des goulots d'étranglement ou des couloirs étroits où les interactions sont prévisibles et limitées. Dans un couloir, un seul conflit résolu peut suffire à débloquer la situation pour de nombreux agents. L'arbre de contraintes reste petit car les interactions sont limitées et prévisibles.	CBS peut devenir moins efficace dans des espaces très ouverts où de multiples chemins de coût équivalent existent. Cela peut générer un très grand nombre de conflits similaires que l'algorithme devra résoudre un par un, augmentant la taille de l'arbre de contraintes. Dans ces cas, résoudre un conflit ne fait souvent que déplacer le problème : les agents trouvent une autre route de même coût qui génère un nouveau conflit un peu plus loin. Cela force CBS à explorer de très nombreuses branches quasi-identiques dans son arbre, le rendant inefficace.

6. Conclusion : Ce qu'il Faut Retenir

Pour résumer, l'algorithme Conflict-Based Search repose sur trois piliers fondamentaux :

1. Une Approche à Deux Niveaux Il sépare le problème entre un "gestionnaire de conflits" de haut niveau qui a une vue d'ensemble et des "planificateurs de chemins" de bas niveau, experts pour un seul agent.
2. Résolution par Contraintes Il ne modifie pas les chemins de manière aléatoire. Il détecte un conflit précis (agent, lieu, temps) et le résout de manière chirurgicale en créant deux scénarios : soit l'agent A évite le conflit, soit l'agent B l'évite.
3. Efficacité Ciblée Sa performance découle du fait que l'effort de recherche est proportionnel au nombre d'interactions problématiques (les conflits), le rendant idéal pour les scénarios où les agents interagissent peu ou de manière prévisible.
