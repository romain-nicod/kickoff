# Skills

Une seule skill, `project-kickoff` : elle applique, avec ce gabarit, la méthode de livraison par
user story (`/Users/albert/Documents/Claude/ObsiClaud/dev/methode/Méthode - Livraison applicative par user story.md`).
**Elle vit ici, versionnée avec les gabarits qu'elle utilise** : une skill et un gabarit modifiés
dans le même commit ne peuvent pas diverger.

| Skill | Répond à | Se déclenche |
|---|---|---|
| **`project-kickoff`** | « Crée le dépôt, le board et les premières US » ; « Prépare le déploiement » | lancement d'un projet, besoin à transformer en US, PR de déploiement |

## Installation : un lien symbolique, pas une copie

`~/.claude/skills/project-kickoff` est un **lien symbolique** vers ce dossier dans le clone
principal. Il n'y a donc rien à recopier après une modification : la skill chargée est celle de la
branche extraite dans `code/kickoff`, normalement `main`. Une branche de travail dans un worktree ne
change pas la skill en service tant qu'elle n'est pas mergée.

Sur une nouvelle machine, depuis son terminal :

```bash
ls -la ~/.claude/skills/
ln -s /Users/albert/Documents/Claude/code/kickoff/skills/project-kickoff ~/.claude/skills/project-kickoff
ls -l ~/.claude/skills/project-kickoff
```

Attendu : une ligne qui commence par `l` et se termine par
`-> /Users/albert/Documents/Claude/code/kickoff/skills/project-kickoff`. Si `ln` répond
« File exists », un dossier ou un lien porte déjà ce nom : regarder ce qu'il contient avant toute
chose, l'archiver dans `~/.claude/skills-archive/` s'il s'agit d'une ancienne copie, puis relancer
`ln`.

`bin/kickoff` retire `skills/` du projet qu'il crée : la skill a fini son travail à ce moment-là.

## Pourquoi il n'y en a qu'une

Les anciennes skills `methode-projet` et `methode-wagon` sont archivées dans
`~/.claude/skills-archive/` et ne reviennent pas : elles portaient une deuxième version de la
méthode, qui la contredisait (RSpec, branches `feat/…`, commentaires en français, spécifications et
plans de tests hors des issues). La méthode fait foi dans la note du vault ; les idiomes Rails encore
valables sont dans `stacks/rails/` (`GOLDEN_RULES.append.md`, `docs/GEMS.md`).
