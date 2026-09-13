<!-- Titre de la PR = titre de l'US. Une PR par US, ouverte quand tout est vert.
     Pour une PR de déploiement, voir .github/PULL_REQUEST_TEMPLATE/deploiement.md. -->

Closes #<!-- US -->
Closes #<!-- chaque [Task] de l'US, une ligne par tâche -->
Dépend de : #<!-- une seule ligne, seulement si l'US dépend d'une autre issue ; sinon la supprimer -->

<!-- Le corps ne cite que son US, ses [Task] et, le cas échéant, sa dépendance.
     Aucune liste d'autres PR ou issues pour le contexte. -->

## ⚠️ Après avoir récupéré cette branche

<!-- Cocher ce que le relecteur doit lancer pour que l'application marche chez lui.
     Supprimer la section si rien ne s'applique. -->

- [ ] `bundle install` — le Gemfile a changé
- [ ] `bin/rails db:migrate` — nouvelle migration
- [ ] `bin/rails db:seed` — les données de démonstration ont changé
- [ ] nouvelle variable dans `.env` — son nom est dans `.env.example`, dire où trouver la valeur
- [ ] autre :

## Ce que ça change

<!-- Ce que Romain verra fonctionner, pas la liste des fichiers. Trois lignes. -->

-

## Fichiers impactés

<!-- Une ligne par fichier : POURQUOI il change, pas ce qu'il contient. -->

-

## Instructions de test

<!-- Les commandes exactes, puis les résultats réels sur le dernier commit. -->

```bash
bin/rails test
bin/rails test:system
bin/rubocop
bin/brakeman --no-pager
bundle exec bundler-audit --update
bin/importmap audit
```

| Contrôle | Résultat | Commit |
|---|---|---|
| `bin/rails test` | <!-- n tests, n assertions, 0 échec --> | `<sha>` |
| `bin/rails test:system` | | `<sha>` |
| Lint et sécurité | | `<sha>` |
| CI | <!-- lien --> | `<sha>` |
| Recette (port 3100) | <!-- intégrée le JJ/MM, parcours testé --> | `<sha>` |

Parcours à suivre en recette :

1.

## UI/UX

<!-- Si l'US touche une page : captures à 1512×982, 1280×800 et 390×844, avec des
     données longues. Aucun défilement horizontal, cibles ≥ 44 px, contraste,
     aucun texte anglais visible, états vides et erreurs qui mènent quelque part.
     Sinon : « sans objet ». -->

## QA idiomatique

<!-- Relecture du diff faite : conventions Rails, helpers natifs, pas de
     factorisation excessive, commentaires d'intention en anglais, rien de mort. -->

- [ ] Diff relu en entier

## Definition of Done

Suivie dans l'issue de l'US : les cases y sont cochées, pas ici.

## Notes de déploiement

<!-- Migration, variable, tâche à lancer, interrupteur à activer, ordre à respecter.
     Repris dans la rubrique « À savoir » du CHANGELOG.md au prochain déploiement.
     Sinon : « aucune ». -->
