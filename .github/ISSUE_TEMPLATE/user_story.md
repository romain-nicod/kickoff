---
name: User story
about: Un parcours utilisateur ou la réponse à un besoin, revu par Romain avant Ready
title: "[US] "
labels: "type:user-story, à revoir par Romain"
---

<!-- Gabarit de la méthode « Livraison applicative par user story » (§ 3 et § 4.7).
     Titre : [US] <besoin ou parcours>. Romain ne lit que les US ; les tâches
     [Task] sont des sous-issues de celle-ci. -->

## État

- Board : **Backlog** — Romain passe l'US en *Ready* après revue, l'agent retire alors le label `à revoir par Romain`.
- Branche : `us-NNN-slug` (créée à l'ouverture de la session) · PR : —

## User story

En tant que <qui>, je veux <quoi>, afin de <pourquoi>.

## Critères d'acceptation

<!-- Vérifiables par quelqu'un d'autre. L'identifiant figure dans le nom du test
     qui le vérifie (`test "CA-01 ..."`) : pas de plan de tests séparé. -->

- [ ] **CA-01** —
- [ ] **CA-02** —
- [ ] **CA-03** —

## Impacts

<!-- Chaque ligne est remplie, ou porte « aucun » explicitement. -->

| Impact | À faire |
|---|---|
| Wireframe (validé à la revue, avant *Ready*) | aucun |
| Documents : schéma de données, wiki (`docs/wiki/`), `README`, `.env.example`, déploiement | aucun |
| Migration de données | aucune |
| Dépendance à une autre US | aucune |

## Hors périmètre

-

## Tâches

<!-- Sous-issues [Task], créées et tenues par l'agent. -->

- [ ] #

## Definition of Done

- [ ] Critères d'acceptation vérifiés un par un
- [ ] Tests unitaires, intégration, système (si interface) et non-régression écrits, vus rouges puis verts
- [ ] Suite complète et CI vertes sur le dernier commit
- [ ] Contrôles de sécurité passés (Brakeman, bundler-audit, `importmap audit`, tests de droits, CSRF, injection, XSS)
- [ ] Passe UI/UX faite, captures jointes à la PR à 1512×982, 1280×800 et 390×844 (si interface)
- [ ] QA idiomatique du diff faite, code commenté
- [ ] US documentée dans le wiki du projet (parcours livré ; schéma d'architecture si la structure change ; ADR si une décision a été prise), `README` et `.env.example` à jour, apprentissages dans le vault
- [ ] Testée en recette
- [ ] PR relue et **mergée par Romain**
- [ ] Déployée en production et vérifiée
