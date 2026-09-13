# Board

Le board GitHub (Projects v2) est **le lieu de coordination** du projet : on y lit d'un coup d'œil ce
qui attend qui. Les règles du cycle font foi dans la méthode
(`/Users/albert/Documents/Claude/ObsiClaud/dev/methode/Méthode - Livraison applicative par user story.md`,
§ 2.1) ; cette page ne dit que comment le board est installé et tenu.

**Board :** <!-- URL affichée par scripts/setup_project.py -->

## Les sept statuts

| Statut | Posé par |
|---|---|
| Backlog | l'agent, à la création d'une `[US]` ou d'un `[BUG]` (label `à revoir par Romain`) |
| Ready | **Romain** |
| In progress | l'agent, à l'ouverture du worktree |
| En recette | l'agent, branche intégrée à la recette, tous les tests verts |
| In review | l'agent, PR ouverte et CI verte |
| À déployer | le workflow du board, au merge |
| Done | l'agent, après le déploiement vérifié |

Un défaut trouvé en recette ou en revue ramène l'US à **In progress**.

## Installation

```bash
gh auth refresh -s project --hostname github.com   # une fois par machine
python3 scripts/setup_project.py --dry-run
python3 scripts/setup_project.py
```

Le script crée le board, le relie au dépôt, pose les sept statuts, ajoute les issues absentes
(ouvertes en *Backlog*, fermées en *Done*) et crée trois vues : *Kanban*, *À revoir par Romain*,
*All items*. Il ne déplace jamais un élément qui a déjà un statut.

⚠️ Réécrire les options de *Status* leur donne de nouveaux identifiants : tous les éléments
perdent leur statut. Sur un board déjà rempli, le script s'arrête ; `--force-statuses` passe outre.

### À faire à la main, une fois

L'API n'expose ni les workflows intégrés ni le regroupement des vues.

1. Ouvrir le board → menu `⋯` en haut à droite → **Workflows**.
2. **Item closed** → activer → *Set value* : `Status` = `À déployer`.
3. **Pull request merged** → activer → `Status` = `À déployer`.
4. **Auto-add to project** → activer → filtre `is:issue is:open` sur ce dépôt.
5. Vue **Kanban** → `⋯` → *Group by* → `Status`.

Si le script n'a pas pu poser les statuts : `Status` → *Edit field* → créer les options dans l'ordre
du tableau ci-dessus, avec ces libellés exacts.

## Déplacer une US

```bash
gh project field-list <n> --owner {{OWNER}} --format json   # id du champ Status et de ses options
gh project item-list <n> --owner {{OWNER}} --format json    # id de l'élément
gh project item-edit --id <élément> --project-id <projet> \
  --field-id <champ Status> --single-select-option-id <option>
```

Aucune GitHub Action à jeton personnel pour ces transitions, sans nécessité démontrée.
