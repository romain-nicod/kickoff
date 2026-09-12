---
name: Défaut
about: Un comportement qui s'écarte d'un critère d'acceptation, en production ou en recette
title: "[Bug] "
labels: "type:bug, à revoir par Romain"
---

## Ce qui se passe

<!-- Une phrase. -->

## Ce qui devrait se passer

<!-- Citer le critère : « #12 CA-03 ». Sans critère à citer, c'est peut-être une
     nouvelle US plutôt qu'un défaut. -->

## Reproduire

1.
2.
3.

- Environnement : production · recette · dev
- Version (`VERSION`) et commit :
- Largeur d'écran et navigateur :
- Compte utilisé (fictif en recette, jamais un vrai mot de passe ici) :

## Gravité

- [ ] **Bloquant** — un parcours principal est cassé ou des données sont en jeu
- [ ] **Majeur** — un critère d'acceptation n'est pas tenu, le parcours survit
- [ ] **Mineur** — cosmétique ou cas limite

## Correction

- [ ] Test de non-régression écrit et vu rouge avant la correction
- [ ] PR qui ferme ce défaut (`Closes #n`), mergée par Romain
- [ ] Livrée dans la version : `vX.Y.Z` (rubrique « Corrections » du `CHANGELOG.md`)
