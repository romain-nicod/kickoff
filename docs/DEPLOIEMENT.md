# Déploiement

Chaque mise en production passe par **sa PR de déploiement**, règle commune à tous les sites et apps
web. La méthode fait foi (§ 6) ; cette page dit comment l'appliquer dans ce dépôt.

## Le cycle d'une version

1. **Tout le lot d'US est mergé par Romain.** Les issues sont en *À déployer*.

   ⚠️ **La PR de déploiement s'ouvre après le merge du lot et se merge en dernier.** Une PR de
   fonctionnalité mergée après elle part en production sans figurer dans la release note (constaté
   sur PEF le 12/09/2026).
2. **L'agent prépare la version** sur une branche partie de `origin/main` :

   ```bash
   git fetch origin
   git switch -c deploy/vX.Y.Z origin/main
   ```

   Il met à jour `VERSION` et ajoute en haut de `CHANGELOG.md` la section `## vX.Y.Z — JJ/MM/AAAA`,
   avec ses trois rubriques (modèle en commentaire dans le fichier). **S'il y a des migrations
   nouvelles, il les relit et les ajoute au garde de déploiement dans cette même branche** : Romain
   voit et approuve dans la PR ce qui part en production. Rien d'autre ne change dans cette branche.
3. **Il ouvre la PR**, titre `[Déploiement] vX.Y.Z`, sur le gabarit dédié. GitHub ne l'applique pas
   tout seul ; deux façons de l'appeler :

   ```bash
   git push -u origin deploy/vX.Y.Z
   gh pr create --base main --head deploy/vX.Y.Z --title "[Déploiement] vX.Y.Z" \
     --body-file .github/PULL_REQUEST_TEMPLATE/deploiement.md
   ```

   ou, dans le navigateur :
   `https://github.com/{{REPO}}/compare/main...deploy/vX.Y.Z?expand=1&template=deploiement.md`
4. **CI verte → Romain relit et merge.**
5. **L'agent déploie le commit de merge** avec le script du projet (ci-dessous).
6. **Il publie la release**, une fois la production vérifiée :

   ```bash
   python3 scripts/publish_release.py --dry-run
   python3 scripts/publish_release.py
   ```

   Le script lit `VERSION` et `CHANGELOG.md` au commit déployé, pose l'étiquette `vX.Y.Z`, la pousse
   et crée la release GitHub avec la section du journal, mot pour mot. Il refuse de déplacer une
   étiquette déjà publiée.
7. **Les US du lot passent en *Done*.** La liste des releases GitHub est le suivi des déploiements.

## Numérotation

`MAJEUR.MINEUR.CORRECTIF`. Le **mineur** augmente pour une version qui apporte au moins une US ; le
**correctif** pour une version qui ne contient que des corrections ; le **majeur** sur décision de
Romain. `VERSION` vaut `0.0.0` tant que rien n'est en production.

## Le script de déploiement du projet

<!-- À remplir au premier déploiement : chemin du script, hôte, commande. -->

**Script :** _à remplir_ · **Production :** _à remplir_

Quel que soit l'hébergement, il fait au minimum, et dans cet ordre :

1. refuser si la CI de ce commit de `main` n'est pas terminée et verte ;
2. refuser toute migration nouvelle absente du garde de déploiement ;
3. sauvegarder la base et les fichiers, et dire où ;
4. déployer **ce commit**, pas l'état d'un dossier de travail ;
5. lancer les migrations, puis vérifier la production (`/up`, un parcours principal) ;
6. revenir à la version précédente si la vérification échoue, et le dire.

## Retour arrière

Un agent ne pousse jamais sur `main` : pas de `git revert` poussé directement. Le retour arrière
redéploie la version précédente, par son étiquette, avec le même script ; la correction suit le
cycle normal (US ou défaut, PR, merge par Romain, nouvelle version de correctif).
