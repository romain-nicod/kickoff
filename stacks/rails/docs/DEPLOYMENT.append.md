## Rails: the migration guard

The deployment script refuses any new migration nobody has reviewed. The guard is a list of
`version:SHA-256 digest` kept in the script (or in a file it reads), and **updated in the deployment
pull request**: Romain sees and approves what is going to production.

For every file of `db/migrate/` missing from `schema_migrations` in production:

1. **review it**: does the previous version of the application still run against the migrated database
   (a rollback that does not touch the database)? Does it delete data? Is it slow on a large table?
2. **compute its digest**:

   ```bash
   shasum -a 256 db/migrate/<version>_<name>.rb
   ```

3. **add it to the guard**, with a comment line: what it does, and the story that brings it;
4. carry it over into the "Migrations" table of the deployment pull request and into the "À savoir"
   heading of `CHANGELOG.md`.

Shape of the guard in a shell script run on the host, `$release` being the folder of the deployed
commit and `$release.applied` the list of versions read from `schema_migrations` in production:

```bash
for migration in "$release"/db/migrate/*.rb; do
  version=$(basename "$migration"); version=${version%%_*}
  if ! grep -qx "$version" "$release.applied"; then
    digest=$(shasum -a 256 "$migration" | cut -d ' ' -f 1)
    case "$version:$digest" in
      # 20260101120000: <what it does> (#<story>)
      20260101120000:<digest>) ;;
      *) echo "Migration to examine before deploying: $version"; exit 4 ;;
    esac
  fi
done
```

A migration changed after its review has a different digest and is refused: that is the point — it gets
reviewed again. A working model: `script/deploy_studio_remote.sh` in the PEF repository.
