# Contribuer

Ce dépôt applique la méthode « Livraison applicative par user story » :
`/Users/albert/Documents/Claude/ObsiClaud/dev/methode/Méthode - Livraison applicative par user story.md`.
Branches, commits, tests, recette, PR, revue et déploiement y font foi ; les spécificités du dépôt
sont dans [AGENTS.md](AGENTS.md), les règles de code dans [GOLDEN_RULES.md](GOLDEN_RULES.md).

Cette page n'ajoute que l'identité des commits, le mode de merge, l'hygiène des branches et une règle
d'écriture.

## Identité des commits

Aucune ligne `Co-authored-by:` (ni `Co-Authored-By:`), dans un commit comme dans une PR. Chaque clone
porte, avant son premier commit, l'identité du compte qui merge ; ses worktrees la partagent :

```bash
git config --local user.name "Romain Nicod"
git config --local user.email 296897605+romain-nicod@users.noreply.github.com
```

Une autre adresse fait apparaître un second auteur dans l'historique de GitHub.

## Merge

Une PR se merge par un **commit de merge**, jamais en squash : elle garde tous ses commits, avec
leurs messages, pour être relue commit par commit. `python3 scripts/setup_repo.py` n'autorise que
ce mode.

## Hygiène des branches

Automatique sur tous les projets (méthode § 6). GitHub supprime la branche distante au merge : le
réglage `delete_branch_on_merge` est posé par `python3 scripts/setup_repo.py`. Le reste revient à
l'agent, depuis le clone principal.

**Après chaque merge constaté**, le worktree et la branche locale de l'US disparaissent. Le merge se
constate par l'API, jamais sur la foi du board ni sur un clone local qui n'a pas encore récupéré
`main`.

```bash
gh api repos/{{REPO}}/pulls/<n° de PR> --jq .merged_at        # une date, sinon s'arrêter
git -C code/{{REPO_NAME}} worktree remove ../{{REPO_NAME}}-worktrees/us-NNN-slug   # refuse un worktree modifié
git -C code/{{REPO_NAME}} branch -D us-NNN-slug
git -C code/{{REPO_NAME}} fetch --prune origin
```

**Une branche fermée sans merge, ou remplacée**, est d'abord sauvegardée en bundle hors du dépôt,
puis supprimée en local et sur GitHub :

```bash
mkdir -p ~/Documents/Claude/projects/{{REPO_NAME}}/branches
git -C code/{{REPO_NAME}} bundle create ~/Documents/Claude/projects/{{REPO_NAME}}/branches/<branche>-AAAAMMJJ.bundle <branche>
git bundle verify ~/Documents/Claude/projects/{{REPO_NAME}}/branches/<branche>-AAAAMMJJ.bundle   # doit répondre « okay », sinon s'arrêter
git -C code/{{REPO_NAME}} push origin --delete <branche>
git -C code/{{REPO_NAME}} branch -D <branche>
```

**Aucune branche `worktree-agent-*` ne survit à la session** qui l'a créée : son worktree et sa
branche sont supprimés avant de rendre la main, avec la même sauvegarde si elle porte un travail non
mergé.

**Contrôle mensuel** : lister ce qui reste et écrire pour chaque branche sa raison d'être (une US
ouverte sur le board) ; sinon, la traiter comme ci-dessus.

```bash
git -C code/{{REPO_NAME}} fetch --prune origin
git -C code/{{REPO_NAME}} worktree list
git -C code/{{REPO_NAME}} branch -vv
gh api repos/{{REPO}}/branches --paginate --jq '.[].name'
```

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
