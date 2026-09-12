## Rails : le garde des migrations

Le script de déploiement refuse toute migration nouvelle que personne n'a relue. Le garde est une
liste `version:empreinte SHA-256` tenue dans le script (ou dans un fichier qu'il lit), et **mise à
jour dans la PR de déploiement** : Romain voit et approuve ce qui part en production.

Pour chaque fichier de `db/migrate/` absent de `schema_migrations` en production :

1. **la relire** : l'ancienne version de l'application tourne-t-elle encore sur la base migrée
   (retour arrière sans toucher la base) ? Supprime-t-elle une donnée ? Est-elle longue sur une grosse
   table ?
2. **calculer son empreinte** :

   ```bash
   shasum -a 256 db/migrate/<version>_<nom>.rb
   ```

3. **l'ajouter au garde**, avec une ligne de commentaire : ce qu'elle fait et l'US qui l'apporte ;
4. la reporter dans le tableau « Migrations » de la PR de déploiement et dans la rubrique « À savoir »
   du `CHANGELOG.md`.

Forme du garde dans un script shell exécuté sur l'hôte, `$release` étant le dossier du commit
déployé et `$release.applied` la liste des versions lues dans `schema_migrations` en production :

```bash
for migration in "$release"/db/migrate/*.rb; do
  version=$(basename "$migration"); version=${version%%_*}
  if ! grep -qx "$version" "$release.applied"; then
    digest=$(shasum -a 256 "$migration" | cut -d ' ' -f 1)
    case "$version:$digest" in
      # 20260101120000 : <ce qu'elle fait> (#<US>)
      20260101120000:<empreinte>) ;;
      *) echo "Migration à examiner avant déploiement : $version"; exit 4 ;;
    esac
  fi
done
```

Une migration modifiée après sa relecture change d'empreinte et se fait refuser : c'est voulu, elle
se relit à nouveau. Modèle en service : `script/deploy_studio_remote.sh` du dépôt PEF.
