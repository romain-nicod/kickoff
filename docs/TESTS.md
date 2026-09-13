# Stratégie de tests

La méthode fait foi (§ 4.3 à 4.5) ; cette page dit comment elle s'applique dans ce dépôt.

## Dans quel ordre

1. Écrire le test à partir du critère d'acceptation, dans ses mots, **son identifiant en tête du
   nom**, en anglais : `test "CA-01 refuses a second vote from the same member"`.
2. Le lancer et **le voir échouer**, pour la bonne raison. Un test qui n'a jamais été rouge n'a rien
   prouvé ; pour un défaut, il est vu rouge sur le code fautif.
3. Écrire le moins de code possible pour le faire passer, puis ranger, test vert.

Aucun plan de tests séparé : l'identifiant du critère dans le nom du test est le lien avec l'issue.

## Ce qui est testé

| Niveau | Quand |
|---|---|
| Unitaire | règles métier, validations, services : chaque borne |
| Intégration | chaque route touchée, pour chaque rôle (anonyme, connecté, administrateur), en HTML et en JSON |
| Système | dès que l'US touche une page : le parcours dans un vrai navigateur, aux trois largeurs de la passe UI/UX |
| Non-régression | tout défaut corrigé |
| Sécurité | droits, CSRF actif, injection par les paramètres, échappement XSS ; aucun outil offensif |

Un code 200 ne prouve rien sur une page : ce qui compte est ce que le navigateur a dessiné.

## Quand

- Pendant le développement : les tests ciblés.
- Avant d'intégrer la branche à la recette : la suite complète, une fois.
- La CI est l'arbitre : **pas de PR tant qu'elle n'est pas verte.** Un script lancé hors CI ne
  compte pas comme test.
