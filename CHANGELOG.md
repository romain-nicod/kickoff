# Changelog

One section per version deployed to production, most recent first. Each section **is** the release
note: `scripts/publish_release.py` carries it, word for word, into the GitHub release of the tag with
the same name, with no second write-up. It is written in the `[Déploiement] vX.Y.Z` pull request
(see [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)).

Numbering `MAJOR.MINOR.PATCH`: the **minor** goes up for a version that brings at least one story, the
**patch** for a version that only holds fixes. `VERSION` stays at `0.0.0` until something is in
production.

<!-- Model of a section, to be copied above the previous one. The three level-3
     headings are required by scripts/publish_release.py, which matches them
     literally: they stay in French, like the pull request's title.

## vX.Y.Z — DD/MM/YYYY

Batch merged from `vX.Y.Z` (`<sha>`) up to `<sha>`.

### User stories et fonctionnalités déployées

- [US] <story title> (#<story>, PR #<PR>)

### Corrections, outillage et documentation

- <pull request title> (#<PR>)

### À savoir

- <shipped but inactive, migration, action expected>, or "Rien de particulier."
-->
