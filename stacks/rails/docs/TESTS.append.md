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

### La barrière

`bin/rails test`, `bin/rails test:system`, `bin/rubocop`, `bin/brakeman --no-pager`,
`bundle exec bundler-audit --update` et `bin/importmap audit` : verts en local, puis en CI, avant
d'ouvrir la PR.
