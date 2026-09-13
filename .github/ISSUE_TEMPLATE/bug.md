---
name: Bug
about: Un défaut constaté (recette, production, revue QA, test instable) — même cycle qu'une US
title: "[BUG] "
labels: "type:bug, à revoir par Romain"
---

<!-- Titre : [BUG] <comportement fautif>. Romain lit les US et les bugs ; comme une US,
     le bug passe par Backlog, puis Ready quand Romain l'a revu. -->

## État

- Board : **Backlog** — Romain passe le bug en *Ready* après revue, l'agent retire alors le label `à revoir par Romain`.
- Branche : (créée à l'ouverture de la session) · PR : —

## Constat

<!-- Ce qui se passe, en une phrase, puis comment le reproduire. -->

1.
2.
3.

- Où : production · recette · CI (test instable) · revue QA
- Version (`VERSION`) et commit :
- Largeur d'écran et navigateur :
- Compte utilisé (fictif ; jamais un vrai mot de passe ici) :

## Comportement attendu

<!-- Citer le critère d'origine quand il existe : « #12 CA-03 ». -->

## Critères d'acceptation

- [ ] **CA-01** — le comportement attendu est rétabli, vérifiable par quelqu'un d'autre
- [ ] **CA-02** — un test de non-régression le prouve, vu rouge sur le code fautif

## Impacts

<!-- Chaque ligne est remplie, ou porte « aucun » explicitement. -->

| Impact | À faire |
|---|---|
| Gravité : bloquant (parcours principal cassé, données en jeu) · majeur (un critère non tenu) · mineur | |
| Données de production à corriger | aucune |
| Documents : wiki (`docs/wiki/`), `README`, `.env.example` | aucun |
| Migration de données | aucune |
| Dépendance à une autre issue | aucune |

## Definition of Done

- [ ] Critères d'acceptation vérifiés un par un
- [ ] Test de non-régression écrit et vu rouge avant la correction, puis vert
- [ ] Suite complète et CI vertes sur le dernier commit
- [ ] Contrôles de sécurité passés (Brakeman, bundler-audit, `importmap audit`)
- [ ] Passe UI/UX faite, captures jointes à la PR à 1512×982, 1280×800 et 390×844 (si interface)
- [ ] QA idiomatique du diff faite, code commenté
- [ ] Piège ajouté à `docs/wiki/Pieges.md` s'il peut toucher d'autres US, apprentissages dans le vault
- [ ] Testé en recette
- [ ] PR relue et **mergée par Romain**
- [ ] Déployé en production et vérifié, listé dans la rubrique « Corrections » du `CHANGELOG.md`
