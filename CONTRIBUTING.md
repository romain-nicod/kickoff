# Contribuer

Ce dépôt applique la méthode « Livraison applicative par user story » :
`/Users/albert/Documents/Claude/ObsiClaud/dev/methode/Méthode - Livraison applicative par user story.md`.
Branches, commits, tests, recette, PR, revue et déploiement y font foi ; les spécificités du dépôt
sont dans [AGENTS.md](AGENTS.md), les règles de code dans [GOLDEN_RULES.md](GOLDEN_RULES.md).

Cette page n'ajoute qu'une règle d'écriture.

## Le livrable, c'est le diff

Viser **le plus petit diff qui fait le travail** : Romain doit voir le changement, pas le chercher.

- Ne jamais toucher l'indentation d'une ligne qu'on ne change pas : un décalage fait paraître dix
  lignes modifiées quand une seule l'est.
- Ne jamais retaper un bloc pour y changer un mot : le risque de perdre une balise fermante est
  réel, et le diff devient illisible.
- Les passes de QA (sécurité, accessibilité, formatage) sont des commits séparés des commits de
  comportement.
- Relire `git diff` avant de dire que c'est fini : un fichier juste peut produire un diff illisible.

Le test avant de pousser : combien de lignes changées pour combien de lignes utiles ? Au-delà de
deux pour une, découper autrement.
