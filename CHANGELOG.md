# Journal des versions

Une section par version déployée en production, la plus récente en haut. Chaque section **est** la
release note : `scripts/publish_release.py` la reprend telle quelle dans la release GitHub de
l'étiquette du même nom, sans deuxième rédaction. Elle s'écrit dans la PR `[Déploiement] vX.Y.Z`
(voir [docs/DEPLOIEMENT.md](docs/DEPLOIEMENT.md)).

Numérotation `MAJEUR.MINEUR.CORRECTIF` : le **mineur** augmente pour une version qui apporte au
moins une US, le **correctif** pour une version qui ne contient que des corrections. `VERSION`
vaut `0.0.0` tant que rien n'est en production.

<!-- Modèle d'une section, à copier au-dessus de la précédente. Les trois titres
     de niveau 3 sont exigés par scripts/publish_release.py.

## vX.Y.Z — JJ/MM/AAAA

Lot mergé depuis `vX.Y.Z` (`<sha>`) jusqu'à `<sha>`.

### User stories et fonctionnalités déployées

- [US] <titre de l'US> (#<US>, PR #<PR>)

### Corrections, outillage et documentation

- <titre de la PR> (#<PR>)

### À savoir

- <livré mais inactif, migration, action attendue>, ou « Rien de particulier. »
-->
