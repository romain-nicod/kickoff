# Le wiki

La méthode range dans le wiki GitHub du projet (§ 1, § 7, Q12) : **chaque US livrée** (parcours,
fonctionnement), **les schémas d'architecture**, **les décisions et ADR**, les guides pratiques. Le
vault n'en garde qu'un lien.

## Une seule source : `docs/wiki/`

Le wiki GitHub est un dépôt à part, que les PR ne montrent pas. Les pages s'écrivent donc dans
`docs/wiki/`, dans la PR de l'US, où Romain les relit ; le workflow `.github/workflows/wiki.yml` les
publie à chaque merge sur `main` qui touche ce dossier.

- Une page par fichier, nommé `Titre-Avec-Tirets.md` : c'est le nom de la page dans le wiki.
- Une page modifiée dans l'interface du wiki est écrasée à la publication suivante.
- Une page retirée de `docs/wiki/` reste dans le wiki : la supprimer à la main.
- Le workflow n'utilise que le jeton fourni par GitHub, aucun jeton personnel.

## Ce qui va où

| Contenu | Où |
|---|---|
| Page d'une US livrée | `docs/wiki/US-NNN-<slug>.md`, dans la PR de l'US |
| Schéma d'architecture | [`docs/wiki/Architecture.md`](wiki/Architecture.md), dans la PR qui change la structure |
| Décision | `docs/wiki/ADR-NNNN-<slug>.md`, et une ligne dans [`Decisions.md`](wiki/Decisions.md) |
| Piège transverse | [`docs/wiki/Pieges.md`](wiki/Pieges.md) |
| Schéma de données | [`docs/SCHEMA.md`](SCHEMA.md) : il change dans le même commit que la migration |
| Commandes, variables | `README.md`, `.env.example` |
| État du projet, apprentissages transverses | le vault |

## Première publication — Romain, une fois

GitHub ne crée le dépôt du wiki qu'à la première page enregistrée à la main.

1. Ouvrir `https://github.com/{{REPO}}/wiki`.
2. Cliquer **Create the first page**, garder le titre `Home`, cliquer **Save page**.
3. Onglet **Actions** → workflow **Wiki** → **Run workflow** → **Run workflow**.
4. Recharger le wiki : la page `Home` est celle de `docs/wiki/Home.md`.

Tant que l'étape 2 n'est pas faite, le workflow l'annonce et se termine sans erreur.

## Publier à la main

```bash
git clone https://github.com/{{REPO}}.wiki.git /tmp/{{REPO_NAME}}.wiki
cp -R docs/wiki/. /tmp/{{REPO_NAME}}.wiki/
git -C /tmp/{{REPO_NAME}}.wiki add -A
git -C /tmp/{{REPO_NAME}}.wiki commit -m "Publication de docs/wiki"
git -C /tmp/{{REPO_NAME}}.wiki push origin HEAD:master
```

Le dépôt d'un wiki n'affiche que la branche `master`.
