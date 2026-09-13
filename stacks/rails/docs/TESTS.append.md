## Rails : Minitest et Capybara

Minitest et les fixtures, le défaut de Rails. Un projet trouvé sous RSpec bascule sur Minitest.

```bash
bin/rails test                               # unitaires et intégration
bin/rails test:system                        # navigateur : bin/rails test ne le lance pas
bin/rails test test/models/vote_test.rb:42   # pendant le développement
bin/rails test -n "/CA-01/"                  # les tests d'un critère
```

### Où vont les tests d'une US

| L'US change | Elle reçoit |
|---|---|
| une règle métier, une validation, un scope | `test/models/`, chaque borne |
| un calcul sorti d'une vue | `test/helpers/` |
| un service, un analyseur | `test/services/` |
| une route : statut, redirection, droits par rôle, HTML et JSON | `test/integration/` |
| une page | `test/system/`, aux trois largeurs |

### Tests système

`test/application_system_test_case.rb` pilote Chrome sans interface par Selenium, et fournit :

- `WIDTHS` et `resize_viewport(width)` : les largeurs CSS exactes de la passe UI/UX, 1512, 1280
  et 390 px ;
- `assert_no_horizontal_overflow(width)` : aucun défilement horizontal, ni sur la page ni dans un
  élément ;
- `assert_reachable_targets(width, selector)` : chaque contrôle est visible et mesure au moins
  44 px.

```ruby
test "CA-02 the vote list fits every screen" do
  WIDTHS.each do |width|
    resize_viewport(width)
    visit votes_path
    assert_no_horizontal_overflow(width)
    assert_reachable_targets(width, "main a.btn, main button")
  end
end
```

Les gems `capybara` et `selenium-webdriver` sont dans le groupe `:test` du `Gemfile` ;
`python3 scripts/after_rails_new.py` signale celle qui manque.

### Pièges déjà payés

- **`rack_test` n'exécute pas Turbo.** Un `POST` qui répond 200 sans rediriger passe dans un test
  d'intégration et échoue dans le navigateur : rediriger, et le vérifier en test système.
- **Fixtures, pas FactoryBot** : une fixture porte le minimum pour être valide.
- **Aucun appel réseau réel** dans la suite : bouchonner le client HTTP.
- **`travel_to`** pour tout ce qui dépend du temps, jamais `sleep`.
- Si la suite parallèle est instable ou lente sur une machine, `PARALLEL_WORKERS=1`, et la raison
  dans `AGENTS.md`.

### Les gardes qu'une suite ne se donne pas seule

Une suite verte dit que le code fait ce que les tests demandent, rien sur ce que personne n'a pensé à
demander. Trois gardes, chacune écrite après un défaut passé à travers une suite verte sur le premier
vrai projet :

| Garde | Le défaut d'où elle vient |
|---|---|
| **Aucune liste ne déborde à 390 px** | une liste sur dix défilait de côté sur téléphone, et la garde en a trouvé une onzième que personne n'avait vérifiée |
| **Chaque langue porte les clés de la source, portée par portée** | une traduction est restée à 56 % pendant une journée, et seul quelqu'un qui comptait pouvait le voir |
| **Aucun écran n'affiche `translation missing`** | deux listes l'affichaient entre leurs contrôles de pagination, et chaque formulaire refusé l'affichait à la place de l'erreur |

- 🔴 **Une garde qui ne peut pas échouer n'est pas une garde.** Casser ce qu'elle surveille, la voir
  rouge, puis rétablir : c'est le « vu rouge » de la méthode, appliqué aux gardes.
- ⚠️ **Parcourir, ne pas échantillonner.** Un chemin de plus dans une garde coûte une ligne ; un
  chemin oublié coûte un écran cassé devant un client. Et **paginer avant de regarder** : une liste
  de trois lignes cache tous les défauts qui vivent dans les contrôles de la deuxième page.

### La barrière

`bin/rails test`, `bin/rails test:system`, `bin/rubocop`, `bin/brakeman --no-pager`,
`bundle exec bundler-audit --update` et `bin/importmap audit` : verts en local, puis en CI, avant
d'ouvrir la PR.
