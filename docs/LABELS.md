# Labels

Un label est un **filtre** : il n'existe que si quelqu'un le cherche ou si un script le lit. Ce qui
dit où en est une US vit dans le board, pas dans un label.

Déclarés dans [`.github/labels.yml`](../.github/labels.yml), créés par
`python3 scripts/setup_repo.py`, qui supprime aussi les neuf labels fournis par GitHub (sauf ceux
qu'une issue porte encore).

| Label | Posé par | Quand |
|---|---|---|
| `type:user-story` | gabarit `[US]` | toute user story ; Romain lit les US et les bugs |
| `Task` | gabarit `[Task]` | action concrète d'une US, en sous-issue de celle-ci ; tenue par l'agent |
| `type:bug` | gabarit `[BUG]` | un défaut constaté en recette, en production, en revue QA, ou un test instable ; même cycle qu'une US |
| `à revoir par Romain` | gabarits `[US]` et `[BUG]` | création par l'agent ; **retiré par l'agent** quand Romain a passé l'issue en *Ready* |
| `status:blocked` | à la main | arrêté par quelque chose d'extérieur à l'US — dire quoi en commentaire |

Dans une organisation qui expose les types natifs d'issue, le type `User story` ou `Task` peut
remplacer le label correspondant ; sur un compte personnel, les labels font foi.

**Ajouter un label** : l'écrire dans `.github/labels.yml` et dans ce tableau, dans le même commit,
puis relancer `python3 scripts/setup_repo.py`. Avant, se demander quelle recherche il sert ; si
personne ne sait le dire, ce n'est pas un label.
