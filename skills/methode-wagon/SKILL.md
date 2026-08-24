---
name: methode-wagon
description: Méthodologie de développement enseignée au bootcamp Le Wagon et niveau de code attendu de Romain — le parcours d'une user story en 12 étapes (US et critères, wireframe, design system, schéma, specs, pseudo-code, branche, code en silo, PR, déploiement, wiki), les idiomes Rails obligatoires (importmap jamais yarn, Stimulus jamais de script inline, simple_form, strong params, dependent: :destroy), le découpage MVC du boilerplate, du Ruby élémentaire, et l'interdiction de refactoriser ce qui marche. À déclencher pour tout code assisté sur ses projets — Ruby, Rails, JS — avant d'ouvrir le premier fichier, et dès qu'il demande comment attaquer une US.
---

# Méthode Le Wagon

Romain est en reconversion, bootcamp Le Wagon **AI Software Development** (batch #2319,
démarré le 6 juillet 2026). Il code des projets réels, avec un vocabulaire technique encore
en construction.

**Le code produit doit ressembler à celui qu'on lui enseigne.** Un code plus court, plus
malin ou plus « pro » que le sien est un mauvais code : il ne pourra ni le relire, ni le
défendre, ni le reprendre seul.

---

> ℹ️ **Les chemins `~/Documents/Claude/ObsiClaud/...` cités ci-dessous sont des notes
> personnelles, non publiées.** Cette skill est autonome sans elles : elles ne font
> qu'ajouter le détail et les sources. Si vous l'installez depuis ce dépôt, ignorez-les
> ou remplacez-les par vos propres notes.

## 0. Le parcours d'une US — l'ordre, avant tout le reste

Coder est l'étape 9 sur 12. Avant d'ouvrir un fichier, **situe la demande dans ce
parcours** et dis à Romain à quelle étape on en est : sauter une étape en amont se paie
toujours en aval (une interface dessinée pour un besoin non formulé, des specs qu'on ne
sait pas écrire faute de critères d'acceptation).

```text
 1. US (As a / I can / So that) + critères d'acceptation, gelés avant les specs
 2. Wireframe — états vide / chargement / erreur / plein, mobile d'abord
 3. Prototype cliquable — seulement si l'interaction est non évidente
 4. Design system — Bootstrap d'abord, composant nouveau ajouté AVANT d'être codé
 5. Schéma de données — types, associations, index, contraintes, dependent:
 6. Specs RSpec — un `it` par critère ; les specs EXISTANTES aussi sont mises à jour
 6 bis. Scénarios Given/When/Then dans `docs/SCENARIOS.md`, mappés par la description du `it`
 7. Pseudo-code en commentaires numérotés
 8. Branche depuis un `main` à jour — UNE story = UNE branche, nommée d'après elle
 9. Code en silo : migration → model → route → controller → view → Stimulus
10. Pull request — description, DoD cochée, CI verte, capture
10 bis. **Proposer les revues** — `/code-review` et `/security-review`. Romain décide
11. Déploiement vérifié EN PRODUCTION, migrations comprises
12. Wiki / mémoire : décisions et pièges, avec leur raison
```

**On ne saute pas d'étape, mais on saute les étapes sans objet.** Une US qui ne touche pas
l'interface n'a ni wireframe ni prototype — le dire est une décision, pas un oubli.

**Le détail de chaque étape, avec ses critères de « fini quand » :**
`~/Documents/Claude/ObsiClaud/le-wagon/methode/Wagon - Cheat sheet US.md`
Les deux portes (a-t-on le droit de commencer / de dire que c'est fini) :
`~/Documents/Claude/ObsiClaud/le-wagon/methode/Wagon - DoR et DoD.md`
Le gabarit d'issue de référence :
`~/Documents/Claude/ObsiClaud/le-wagon/methode/Wagon - Template US.md`

🔴 **La description du `it` est un livrable, pas un commentaire.** Elle est
recopiée telle quelle dans `docs/SCENARIOS.md`, où elle sert de clé de mapping —
on ne référence jamais un numéro de ligne, qui serait faux dès la ligne suivante
insérée. Écrire `it "refuse un second vote du même membre"` plutôt que
`it "works"` n'est donc pas de la coquetterie : c'est ce qui rend le scénario
retrouvable avec `rspec -e`.

🔴 **Le TDD porte aussi sur les specs DÉJÀ écrites.** Une US qui touche du code
déjà couvert change ce que ce code doit faire : la spec qui décrivait l'ancien
comportement devient fausse. La mettre à jour fait partie de l'US, pas d'une
passe de nettoyage. **La suite est verte avant la PR** — pas verte « sauf trois
qu'on regardera plus tard ».

🔴 **Avant qu'une US parte : proposer les revues, et attendre la réponse.**

| Revue | Ce qu'elle cherche | Commande |
|---|---|---|
| Revue de code | Bugs de correction, réutilisation, simplifications | `/code-review` |
| Revue de sécurité | Failles introduites par le diff | `/security-review` |

**Je propose, Romain décide** — à chaque US, sans exception. Une revue qui se
déclenche toute seule finit par être ignorée ; une revue refusée est une
décision, et elle se note dans la PR.

**Cadence plancher : une revue de code ET une revue de sécurité par semaine**,
même si aucune US ne les a déclenchées. C'est le minimum, pas le plafond : une
US qui touche l'authentification, un paiement, un upload ou des données
personnelles se fait relire quel que soit le jour.

🔴 **Une user story = une branche, et la branche porte son nom.** Pas de branche
qui porte deux stories, pas de story étalée sur deux branches. Le nom se **dérive
du titre de l'US** — `<type>/<entite>-<action>` — il ne s'invente pas :

```text
« As a visitor, I can see the list of recipes »   →  feat/recipe-list
« As a user, I can create a recipe »              →  feat/recipe-create
« Corriger la validation du formulaire »          →  fix/recipe-validation
```

Si le titre de la story ne donne ni entité ni action claires, ce n'est pas le
nommage qui coince : **la story est trop vague ou trop grosse.** Le nom de
branche est le premier révélateur d'une US mal découpée — le dire à ce
moment-là, pas après avoir codé.

🔴 **Les critères d'acceptation se gèlent avant l'étape 6.** Après le gel, un critère qui
change n'est pas une correction : c'est une nouvelle US.

---

## 0 bis. Écrire idiomatique — ce n'est pas du style

Le code produit doit suivre les conventions **telles qu'elles sont enseignées**, pas telles
qu'on les écrirait « bien » ailleurs. La liste complète, sourcée deck par deck :
`~/Documents/Claude/ObsiClaud/le-wagon/methode/Wagon - Idiomes Rails.md`

Les plus coûteuses à violer :

- 🔴 **JS dans Rails : `./bin/importmap pin <package>`, JAMAIS `yarn add`** — c'est la
  convention Rails, et elle est enseignée comme non négociable. Une librairie posée par
  yarn n'est pas servie par importmap : elle disparaît en production **sans erreur
  serveur**.
- **Comportement JS = contrôleur Stimulus + attributs `data-`**, jamais un `<script>` inline
  ni `querySelector`/`addEventListener` à la main.
- **`simple_form_for`**, pas `form_with` — les classes Bootstrap viennent avec.
- **Strong params** systématiques ; `resources ... only: [...]` plutôt que les 7 routes ;
  un seul niveau de nesting, et sur les actions de collection uniquement.
- **`dependent: :destroy` explicite**, index sur chaque clé étrangère, **Active Storage**
  (jamais une colonne `photo_url`) avec Cloudinary en production.
- **Les helpers Rails, systématiquement** : `link_to` et non un `<a href>` écrit à la
  main, `image_tag` et non un `<img>`, plus `pluralize`, `number_to_currency`,
  `time_ago_in_words`. Le helper gère ce qu'on oublie — échappement, `alt`, pluriels.
- **Les path helpers** (`recipes_path`, `recipe_path(@recipe)`), jamais une URL en dur :
  une URL écrite à la main ne suit pas un changement de routes et casse en silence.
- **Un helper dans `app/helpers/`** dès qu'une vue calcule quelque chose pour l'affichage.
  La vue affiche, elle ne décide pas — et un helper se teste seul.
- **Les helpers que les gems du boilerplate apportent déjà**, plutôt que la balise
  écrite à la main : `simple_form_for` / `f.input` / `f.association` (simple_form),
  `current_user` et `user_signed_in?` (devise), `icon(...)` (font-awesome-sass),
  `cl_image_tag` (cloudinary), `image_tag objet.photo` (Active Storage),
  `policy(objet).update?` (pundit). Avant d'écrire une balise ou une URL dans une vue,
  vérifier qu'une gem installée ne la produit pas mieux — la réponse est souvent oui.
- 🔴 **Le style vit dans un fichier `.scss`, jamais dans la vue** : pas de
  `style="..."` sur une balise, pas de `<style>` dans un template. C'est la même
  règle que pour le JavaScript — le comportement va dans Stimulus, l'apparence
  va dans le SCSS. Un style écrit dans le HTML échappe au design system et ne se
  retrouve pas : personne n'ouvre une vue pour chercher une couleur.
- **Partial : données en `locals`**, jamais une variable d'instance. **SCSS : un seul
  niveau d'imbrication.**
- **`redirect_to` après un POST réussi** — convention Rails, et exigence de Turbo : un POST
  qui ne redirige pas est rejeté en silence.
- 🔴 **Toutes les clés dans `.env`, jamais poussé** — `ENV.fetch("NOM")` dans le
  code, le nom de la variable dans `.env.example` au même commit, secrets de
  l'hébergeur en prod. Une seule mécanique, sans exception « juste pour ce test »
  (règle d'or 28).
- 🔴 **Le test d'abord, à chaque US.** On écrit la spec RSpec depuis le critère
  d'acceptation, **on la regarde échouer**, puis on écrit le minimum qui la fait
  passer. Un test écrit après teste le code ; un test écrit avant teste l'US —
  ils se ressemblent dans le diff et ce n'est pas le même objet. Et un critère
  qu'on n'arrive pas à transformer en test qui échoue est un critère qui n'était
  pas assez précis : le découvrir avant de coder coûte une heure, le découvrir à
  la démo coûte la démo.

Quand tu écris une forme hors de cette liste alors qu'une forme idiomatique existe,
**dis-le et propose l'idiomatique** — ne tranche pas en silence.

---

## 1. Décomposer AVANT d'écrire

C'est le geste central du bootcamp. Avant la première ligne de vrai code, on écrit les
**étapes numérotées en commentaires**, puis on les remplit une par une.

```ruby
def mark_as_done
  # 1. Afficher la liste avec les index
  # 2. Demander l'index à l'utilisateur
  # 3. Récupérer la tâche dans le repository
  # 4. La marquer comme faite
end
```

**Les commentaires numérotés restent dans le code livré.** Ce ne sont pas des brouillons :
c'est ce qui rend la méthode relisable. Le cours les conserve, nous aussi.

La même méthode s'applique au JS (« *Let's pseudocode!* » avant un `fetch`) : lister les
étapes, puis coder.

**Si une étape ne tient pas en une ligne de commentaire, c'est qu'elle mérite sa propre
méthode.** C'est le critère de découpage à utiliser — pas une règle de longueur.

---

## 2. Coder en silo

Une **tranche verticale complète**, testée, avant de commencer la suivante.

En Rails, le flux est : `route ➡️ controller#action ➡️ view`.

**Fais ça :** la route de la page A → l'action de A → la vue de A → vérifier A dans le
navigateur. *Ensuite seulement*, la page B.

**Ne fais pas ça :** les 4 routes, puis les 4 actions, puis les 4 vues. À la première
erreur, douze pièces sont suspectes au lieu de trois.

Hors Rails, même principe : une méthode qui marche de l'entrée à la sortie avant d'écrire
la deuxième ; un composant affiché et vérifié avant le suivant.

---

## 3. Le découpage du boilerplate

L'architecture enseignée (Cookbook, Food Delivery) et le rôle **exclusif** de chaque fichier.
C'est la structure à reproduire dans un programme Ruby en ligne de commande :

| Fichier | Rôle | Interdits |
|---|---|---|
| `app.rb` | Câble les instances et lance le router | Aucune logique métier |
| `router.rb` | Affiche le menu, `case/when` qui appelle le contrôleur | Ne touche ni au model ni au repository |
| `controllers/` | Orchestre : demande à la vue, agit sur le repository | **Aucun `puts` ni `gets`** |
| `repositories/` | Stocke, charge/sauve le CSV, `create/all/find/destroy`, gère les `id` | N'affiche rien |
| `models/` | Données + comportement métier | Ne s'affiche pas, ne se persiste pas |
| `views/` | **Seule** à faire `puts` et `gets` | Aucune décision métier |

```ruby
# app.rb — le câblage, et rien d'autre
repository = TaskRepository.new
controller = TasksController.new(repository)
router     = Router.new(controller)
router.run
```

**La règle qui tranche 90 % des questions : un `puts` ou un `gets` en dehors d'une view est
une erreur d'architecture.** Si un contrôleur a besoin d'afficher, il appelle la vue.

En Rails, c'est la même séparation, avec la *convention over configuration* :
`PagesController#about` → `app/views/pages/about.html.erb`. Respecter le nommage évite
d'avoir à configurer quoi que ce soit.

---

## 4. Le niveau de code attendu

Il a vu, dans l'ordre : Ruby (types, conditions, boucles, méthodes, Array, Hash, blocs,
regex, parsing) → OOP (classes, `attr_*`, `private`, héritage, `super`, méthodes de classe,
`self`) → SQL et ActiveRecord → HTML/CSS/Bootstrap, JS et DOM → Rails (MVC, CRUD,
associations, Devise, upload) → IA (LLM, prompt engineering, embeddings/RAG, agents).

```ruby
# ✅ Ce qu'il lit sans effort
factures.each { |facture| puts facture.total }
recentes = factures.select { |f| f.date > 1.month.ago }
total    = factures.map(&:total).sum

class Facture
  attr_reader :client, :total          # jamais un reader écrit à la main
  def initialize(attributes = {})      # hash d'attributs quand il y en a plusieurs
    @client = attributes[:client]
  end
end

# ❌ Ce qui le bloque
factures.each_with_object(Hash.new(0)) { |f, h| h[f.client] += f.total }
factures.group_by(&:client).transform_values { |fs| fs.sum(&:total) }
define_method(:"total_#{type}") { ... }
```

À éviter sauf demande explicite : métaprogrammation, `send`, `reduce`/`inject`,
Concerns maison, service objects, `&.` en cascade, one-liners denses.

Quand une méthode moins connue est vraiment le bon outil (`group_by`, `sum`, `find_by`),
utilise-la **et ajoute un commentaire d'une ligne disant ce qu'elle retourne**.

Quand tu emploies une syntaxe qui n'était pas au programme, **dis-le explicitement** :
« ceci n'était pas dans le cours, voilà ce que ça fait ».

**Déboguer :** `binding.pry` (gem `pry-byebug`), pas une avalanche de `puts`. C'est ce que
le cours impose dès l'OOP.

---

## 5. Ne pas refactoriser

**Ne touche jamais à du code qui marche sans qu'il l'ait demandé.** Même si tu vois mieux.

- Pas de renommage « au passage » de variables ou de méthodes existantes.
- Pas d'extraction de méthode/module pour factoriser deux bouts qui se ressemblent.
  **Deux fois le même code est acceptable.** À la troisième, tu le signales — tu ne le fais pas.
- Pas de réécriture d'une boucle qui fonctionne en version plus concise.
- Pas de changement d'architecture non demandé.

Nuance importante : **l'héritage, lui, est enseigné comme la réponse au DRY** (`Wizard` et
`Warrior` → `Character`, puis `super`). Si deux classes partagent réellement leur état et
leur comportement dès la conception, propose la classe parente — mais au moment de la
conception, pas en refonte d'un code déjà livré.

Si tu vois un vrai problème (bug, faille, dette coûteuse), **dis-le en une ou deux phrases
et continue la tâche demandée**. Décider de nettoyer lui appartient.

---

## 5 bis. DRY et responsabilité unique — le juste milieu

**Romain aime ces deux principes et les applique de lui-même** (sur Skill Forge, il a
sorti ses system prompts dans des fichiers de configuration). Ne les lui refuse pas — mais
ne les pousse pas à l'extrême non plus : il débute, et il doit pouvoir **comprendre** le
code qu'il livre.

### Une seule question tranche DRY

Avant de factoriser deux bouts qui se ressemblent :

> **« Si cette règle change, dois-je TOUJOURS changer les deux, de la même façon ? »**

- **Oui** → c'est la même décision écrite deux fois. Vraie duplication, factorise.
- **Non** → ils se ressemblent par hasard. **Laisse-les séparés.** Les fusionner crée un
  couplage entre deux choses qui vont diverger, et c'est là qu'on se retrouve avec des
  paramètres booléens partout pour rattraper le coup.

**DRY porte sur les décisions, pas sur les caractères.** Deux fonctions de dix lignes
identiques qui répondent à deux règles métier différentes ne sont pas une duplication.

### La règle des 3

Deux occurrences se tolèrent. On factorise **à la troisième**. À deux, on ne voit pas
encore la forme de l'abstraction — on la devine, et **une mauvaise abstraction coûte plus
cher qu'une copie** : tout le monde la contourne au lieu de la supprimer.

Le coût est asymétrique, et c'est l'argument à lui donner : supprimer une copie prend cinq
minutes ; défaire une abstraction que dix fichiers utilisent prend une journée.

### Sortir une valeur dans un fichier de configuration

C'est sa pratique, et elle est bonne — encadrée. Propose-la quand **les trois réponses sont
oui** :

1. La valeur change **sans que le code change** ? (un prompt, un seuil, une liste de
   libellés, une URL d'API)
2. On veut la modifier **sans lire le code autour** ?
3. Il y en a **plusieurs**, ou il y en aura ?

**Une seule valeur lue à un seul endroit reste dans le code**, nommée en constante en haut
du fichier. Un fichier de configuration à une entrée n'ajoute qu'un fichier de plus à
ouvrir.

Quand tu extrais, trois garde-fous, toujours :

- **Un seul endroit lit le fichier** et le donne au reste du code. Des lectures éparpillées,
  c'est la même valeur avec plusieurs vérités.
- **Une valeur par défaut**, et un **échec clair** si l'entrée manque ou est malformée —
  sinon on a troqué un bug visible contre un bug silencieux.
- **Jamais un fichier `utils` ou `helpers` fourre-tout.** Un fichier dont la responsabilité
  est « divers » est l'exact contraire d'une responsabilité unique.

### 🔴 Les deux tests d'arrêt

1. **« Peut-on encore expliquer un comportement en ouvrant deux fichiers ? »** S'il en faut
   quatre, l'extraction a coûté plus qu'elle n'a rapporté, quelle que soit la théorie.
2. **« Est-ce que je sais lui expliquer cette extraction en trois lignes ? »** Si non, ne la
   fais pas. Une abstraction qu'il ne comprend pas est une abstraction qu'il n'osera pas
   modifier — et il travaillera autour.

Et quand tu extrais, **dis-le et dis pourquoi** : quelle règle est désormais écrite à un
seul endroit, et ce qui casserait si elle était écrite à deux.

⚠️ Cette section dit **comment** factoriser quand c'est le moment. Elle ne lève pas le §5 :
on ne refactorise pas du code qui marche sans qu'il l'ait demandé. Le bon moment pour
appliquer DRY, c'est **en écrivant** le troisième cas, pas en rouvrant les deux premiers.

---

## 6. Livrer

- **Nomme les fichiers dans l'ordre du flux** en l'expliquant — « la route, puis l'action,
  puis la vue » — ça renforce le modèle mental.
- **Une étape vérifiable à la fois** : dis l'URL à ouvrir, la commande à lancer, ce qu'il
  doit voir.
- **Commentaires en français**, identifiants en anglais — sauf terme métier francophone plus
  clair (`facture`, `remise`, `adherent`).
- **Commits en français**, format `"Sujet : détail"`, fonctionnalité et sécurité séparées.
- Les manipulations qui lui incombent (token, OAuth, dashboard) : **pas-à-pas numéroté**,
  URL complète, libellés exacts, et ce qu'il doit voir à la fin.
- Jamais de secret en dur : `.env` local, `.env.example` versionné.

---

## 7. Le Référentiel

Sa bibliothèque de syntaxe personnelle — Ruby, regex, parsing, Terminal/Bash, Git :

- En ligne : https://ai-gmented-pm.github.io/le_wagon_learning/content/reference/referentiel.html
- Source : `~/Documents/Claude/code/le_wagon_learning/content/reference/referentiel.html`

**Aligne tes explications sur ses formulations** : mêmes mots, mêmes exemples, pour qu'il
y retrouve la trace. Quand tu lui apprends quelque chose de réutilisable (commande, piège,
snippet), **propose de l'ajouter au Référentiel** — jamais sans son accord.
