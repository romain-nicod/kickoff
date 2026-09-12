# Pièges transverses

Pièges qui touchent plusieurs US. Chaque entrée dit ce qui arrive, et ce qu'il faut faire à la place.
Les notes propres à une US restent dans sa page.

- `bin/rails test` ne charge pas `test/system` : lancer aussi `bin/rails test:system`, en local
  comme en CI.
- Selenium fait défiler jusqu'à un contrôle masqué avant de cliquer dessus : un test système qui
  clique d'abord atteint un bouton que personne ne voit. Mesurer la mise en page **avant** tout clic
  (`assert_no_horizontal_overflow`, `assert_reachable_targets`).
- Une largeur comparée à `innerWidth` ne prouve rien sur mobile : la mise en page grandit avec son
  propre débordement. Comparer à la largeur émulée.
