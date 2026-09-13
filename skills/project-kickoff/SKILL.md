---
name: project-kickoff
description: Lancer un projet web Rails depuis le gabarit kickoff en appliquant la méthode de livraison par user story — dépôt, AGENTS.md de 25 lignes, labels, board aux sept statuts, wiki, recette locale, issues [US], [Task] et [BUG] sur gabarit, PR de déploiement et release notes. Use when starting a new project ("kick off", "new project", "nouveau projet", "lancer un projet", "set up the repo", "bootstrap"), when turning a need into user stories on a board, or when preparing a [Déploiement] pull request and its GitHub release.
---

# Lancer un projet avec kickoff

**La méthode fait foi** :
`/Users/albert/Documents/Claude/ObsiClaud/dev/methode/Méthode - Livraison applicative par user story.md`.
La lire une fois, en commençant par le résumé en 8 lignes et le § 10 bis ; revenir au reste quand une
question se pose. Cette skill ne la recopie pas : elle dit **quels gestes font, avec le gabarit
`romain-nicod/kickoff`, ce que la méthode demande.**

Aucune mention de l'assistant ni de son éditeur dans le dépôt, les issues, les PR et les commits, et
aucune ligne `Co-authored-by:` (ni `Co-Authored-By:`) dans un commit ou une PR.

---

## 1. Poser le terrain

Demander une seule fois ce qui ne se déduit pas :

| Valeur | Sert à |
|---|---|
| Nom du projet et une phrase | `kickoff.yml`, README |
| Dépôt `propriétaire/nom` | nouveau dépôt privé sur le **compte personnel** (Q8) |
| Dossier du projet dans le vault | première ligne d'`AGENTS.md` |
| Hébergement de production, s'il est connu | `AGENTS.md`, `docs/DEPLOIEMENT.md` |
| Le besoin, sous n'importe quelle forme | les premières `[US]` |

Vérifier le compte actif avant de créer quoi que ce soit : `gh api user --jq .login`.

## 2. Créer le dépôt

```bash
gh repo create <propriétaire>/<nom> --template romain-nicod/kickoff --private --clone
```

Le clone vit dans `~/Documents/Claude/code/<nom>`. Remplir les cinq valeurs de `kickoff.yml`, puis :

```bash
# L'identité du compte qui merge, avant le premier commit ; les worktrees du clone la
# partagent. Une autre adresse fait ajouter un co-auteur par GitHub à chaque merge en squash.
git config --local user.name "Romain Nicod"
git config --local user.email 296897605+romain-nicod@users.noreply.github.com
bin/kickoff --dry-run
bin/kickoff
rails new -d postgresql \
  -m https://raw.githubusercontent.com/romain-nicod/rails-ready/main/template.rb --skip .
python3 scripts/after_rails_new.py
```

`after_rails_new.py` signale les gems manquantes (`capybara`, `selenium-webdriver`,
`sentry-rails`) : les ajouter, `bundle install`. Dans le même geste :

- créer le dossier vault du projet et sa carte, reliés au graphe ;
- inscrire le dépôt dans `ObsiClaud/dev/Dépôts AI-GMENTED.md` (ligne, paragraphe, recouvrement) ;
- vérifier `git check-ignore -v .env` avant le premier push.

## 3. Configurer GitHub

Dans cet ordre — **les labels d'abord** : GitHub retire sans rien dire un label qui n'existe pas
d'une issue créée sur gabarit.

```bash
python3 scripts/setup_repo.py --dry-run && python3 scripts/setup_repo.py
gh auth refresh -s project --hostname github.com
python3 scripts/setup_project.py --dry-run && python3 scripts/setup_project.py
```

Labels : `type:user-story`, `Task`, `type:bug`, `à revoir par Romain`, `status:blocked`. Board :
`Backlog · Ready · In progress · En recette · In review · À déployer · Done`.

Donner ensuite à Romain, pas à pas, ce que l'API ne fait pas :

- les workflows du board et le regroupement du Kanban : `docs/BOARD.md`, « À faire à la main » ;
- la première page du wiki : `docs/WIKI.md`, « Première publication ».

## 4. `AGENTS.md` de 25 lignes au plus

Remplir les emplacements laissés par `bin/kickoff` : URL du board (affichée par
`setup_project.py`), production, script de déploiement. **Seulement les spécificités du projet** :
jamais la méthode. Les pièges vont dans `docs/wiki/Pieges.md`, les décisions dans une page ADR de
`docs/wiki/`. `CLAUDE.md` reste à trois lignes. Contrôle : `wc -l AGENTS.md CLAUDE.md`.

## 5. Créer les issues sur gabarit

**Un besoin de Romain devient une `[US]` sans attendre** ; un besoin trop gros devient plusieurs
US. Le corps suit `.github/ISSUE_TEMPLATE/user_story.md` : état, story, critères `CA-01…`, impacts
(chacun rempli ou « aucun »), hors périmètre, tâches, DoD. Écrire le corps dans un fichier du
bloc-notes, jamais dans le dépôt.

```bash
gh issue create --repo <propriétaire>/<nom> --title "[US] <besoin ou parcours>" \
  --label "type:user-story" --label "à revoir par Romain" --body-file <corps.md>
gh project item-add <n> --owner <propriétaire> --url <URL de l'issue>
```

- **`[Task] <action concrète>`** sur `task.md`, label `Task`, rattachée à l'US en sous-issue :

  ```bash
  id=$(gh api repos/<propriétaire>/<nom>/issues/<n° de la tâche> --jq .id)
  gh api repos/<propriétaire>/<nom>/issues/<n° de l'US>/sub_issues -F sub_issue_id="$id"
  ```

- **`[BUG] <comportement fautif>`** sur `bug.md`, labels `type:bug` et `à revoir par Romain` : un
  défaut constaté en recette, en production, en revue QA, ou un test instable. Même cycle qu'une US.
- À partir de trois issues à revoir : note vault `<Projet> - Revue des US - AAAAMMJJ`, une case et
  une ligne de commentaire par issue.
- **Romain passe en *Ready*.** L'agent retire alors le label :
  `gh issue edit <n> --remove-label "à revoir par Romain"`.

## 6. Pendant les US — les commandes, la méthode fait foi

- Worktree et branche : `git -C code/<nom> worktree add -b us-NNN-slug ../<nom>-worktrees/us-NNN-slug origin/main`.
- Changer un statut (*In progress*, *En recette*, *In review*, *Done*) : `docs/BOARD.md`,
  « Déplacer une US ».
- Tests : `docs/TESTS.md` ; PR sur `.github/PULL_REQUEST_TEMPLATE.md`, `Closes` pour l'US et chaque
  tâche.
- Recette : création, reconstruction à chaque lot et `bin/recette prepare` dans `docs/RECETTE.md`.
- **Jamais de merge vers `main`** : Romain seul merge. Seule la branche locale `recette` reçoit des
  merges de l'agent.
- **Hygiène des branches, automatique** : `setup_repo.py` active la suppression des branches au
  merge. Après chaque merge constaté par l'API (`gh api repos/<propriétaire>/<nom>/pulls/<n> --jq
  .merged_at`), supprimer le worktree et la branche locale de l'US. Une branche fermée sans merge ou
  remplacée est sauvegardée en bundle (`git bundle verify` doit répondre « okay »), puis supprimée en
  local et sur GitHub. Aucune branche `worktree-agent-*` ne survit à sa session. Contrôle mensuel
  des branches restantes. Commandes : `CONTRIBUTING.md`, « Hygiène des branches ».

## 7. Déployer un lot

1. **Attendre que tout le lot soit mergé.** La PR de déploiement s'ouvre après et **se merge en
   dernier** : une PR mergée après elle partirait sans figurer dans la release note.
2. Branche `deploy/vX.Y.Z` depuis `origin/main` : `VERSION`, section `## vX.Y.Z — JJ/MM/AAAA` en
   haut de `CHANGELOG.md` avec ses trois rubriques, et **le garde des migrations** mis à jour
   (`docs/DEPLOIEMENT.md`, section Rails).
3. PR `[Déploiement] vX.Y.Z` :

   ```bash
   gh pr create --base main --head deploy/vX.Y.Z --title "[Déploiement] vX.Y.Z" \
     --body-file .github/PULL_REQUEST_TEMPLATE/deploiement.md
   ```

4. CI verte, Romain merge. Déployer **le commit de merge** avec le script du projet.
5. Production vérifiée, puis :

   ```bash
   python3 scripts/publish_release.py --dry-run
   python3 scripts/publish_release.py
   ```

6. Les issues du lot passent en *Done*.

## 8. Pièges

- `setup_project.py` refuse de réécrire les statuts d'un board déjà rempli : les options de
  *Status* changeraient d'identifiant et chaque élément perdrait le sien.
- Le dépôt d'un wiki n'affiche que `master` ; le workflow *Wiki* ne publie rien tant que Romain n'a
  pas créé la première page.
- `publish_release.py` refuse de déplacer une étiquette déjà publiée : une correction prend un
  nouveau numéro.
- Un secret ne passe jamais par la conversation ni par la ligne de commande : les secrets de l'hôte
  se saisissent par Romain, pas à pas.

## Ce qui fait foi

| Sujet | Où |
|---|---|
| Le cycle de livraison | la note de méthode du vault |
| Gabarits, scripts, stack Rails, cette skill | le dépôt `kickoff` ; `~/.claude/skills/project-kickoff` est un lien symbolique vers `skills/project-kickoff` de son clone principal |
| Les règles d'un projet | son `AGENTS.md` |
| Le générateur de l'application | `rails-ready` |
