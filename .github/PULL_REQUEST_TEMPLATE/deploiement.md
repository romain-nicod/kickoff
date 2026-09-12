<!-- PR de déploiement — titre « [Déploiement] vX.Y.Z », branche `deploy/vX.Y.Z`.
     GitHub n'applique pas ce gabarit tout seul. Deux façons de l'appeler :
       gh pr create --base main --head deploy/vX.Y.Z --title "[Déploiement] vX.Y.Z" \
         --body-file .github/PULL_REQUEST_TEMPLATE/deploiement.md
     ou ouvrir https://github.com/<propriétaire>/<dépôt>/compare/main...deploy/vX.Y.Z?expand=1&template=deploiement.md
     Mode d'emploi complet : docs/DEPLOIEMENT.md.

     ⚠️ Cette PR s'ouvre APRÈS le merge de tout le lot et se merge EN DERNIER. Une PR de
     fonctionnalité mergée après elle partirait en production sans figurer dans la
     release note. -->

## Version

- `VERSION` : `X.Y.Z` (précédente : `X.Y.Z`) — **mineur** si le lot apporte au moins une US, **correctif** s'il ne contient que des corrections
- Production actuelle : commit `…`
- Lot : toutes les PR mergées depuis `vX.Y.Z` jusqu'à `…`

## Release note

La section `## vX.Y.Z — JJ/MM/AAAA` de `CHANGELOG.md`, visible dans le diff de cette PR, **est** la release note : elle n'est pas recopiée ici. Elle porte trois rubriques :

- [ ] *User stories et fonctionnalités déployées* — titre de l'US, numéro, PR
- [ ] *Corrections, outillage et documentation*
- [ ] *À savoir* — ce qui est livré mais inactif, migrations, actions attendues

## Migrations qui partent en production

<!-- Le garde de déploiement se met à jour DANS cette PR : Romain y voit et approuve
     chaque migration avant qu'elle parte. Une ligne par migration nouvelle, ou
     « aucune ». -->

| Migration | Empreinte SHA-256 | Relue : réversible sans toucher la base ? |
|---|---|---|
| aucune | | |

## Avant le merge — Romain

- [ ] Plus aucune PR du lot n'attend son merge : celle-ci est la dernière
- [ ] CI verte sur le dernier commit de `deploy/vX.Y.Z`
- [ ] Le diff ne touche que `VERSION`, `CHANGELOG.md` et le garde des migrations
- [ ] Chaque migration du tableau ci-dessus est relue et approuvée
- [ ] Rien dans « À savoir » ne demande une action préalable qui n'a pas été faite

## Après le merge — agent

- [ ] Déployer **le commit de merge** avec le script du projet : CI verte, sauvegarde, retour arrière, vérification
- [ ] `python3 scripts/publish_release.py` : étiquette `vX.Y.Z` et release GitHub depuis la section du journal
- [ ] Vérification en production : <!-- URL et parcours contrôlés -->
- [ ] US du lot passées en *Done*

## Retour arrière

<!-- La commande exacte du script du projet et l'emplacement de la sauvegarde prise
     avant le déploiement. -->
