require "test_helper"

# Browser tests: real Chrome, real CSS, real JavaScript.
#
# Run with `bin/rails test:system`: `bin/rails test` does not load
# test/system, and the CI runs both.
#
# A GET 200 proves nothing about a layout. The helpers below measure what
# the browser drew, BEFORE any click: Selenium scrolls a clipped control
# into view on its own, so a test that clicks first reaches a button
# nobody can see.
class ApplicationSystemTestCase < ActionDispatch::SystemTestCase
  # The three screens of the UI/UX pass of the delivery method.
  SCREENS = { 1512 => 982, 1280 => 800, 390 => 844 }.freeze
  WIDTHS = SCREENS.keys.freeze

  driven_by :selenium, using: :headless_chrome,
                       screen_size: [ 1512, 982 ] do |options|
    # GitHub runners start Chrome as root in a small container.
    if ENV["CI"]
      options.add_argument("--no-sandbox")
      options.add_argument("--disable-dev-shm-usage")
    end
  end

  teardown do
    # The emulation belongs to the browser, which Capybara reuses from one
    # test to the next.
    page.driver.browser.execute_cdp("Emulation.clearDeviceMetricsOverride")
  end

  private

  # Exact CSS viewport, independent of the window chrome. Under 768 px
  # Chrome also behaves as a phone (touch, mobile viewport).
  def resize_viewport(width, height = SCREENS.fetch(width, 900))
    page.driver.browser.execute_cdp(
      "Emulation.setDeviceMetricsOverride",
      width: width, height: height, deviceScaleFactor: 1,
      mobile: width < 768
    )
  end

  # No horizontal scroll, on the document AND inside any element.
  #
  # Compared with the EMULATED width, never with `innerWidth`: on a mobile
  # viewport the layout grows with its own overflow. The offenders are the
  # boxes past the right edge and the containers that scroll OR clip
  # sideways: clipping a button is not fitting it.
  def assert_no_horizontal_overflow(width, root: "body")
    offenders = page.evaluate_script(<<~JS, width, root)
      (function (width, root) {
        const found = [];
        const html = document.documentElement;
        if (html.scrollWidth > width + 1 || window.scrollX !== 0) {
          found.push({ element: "document",
                       scrollWidth: html.scrollWidth });
        }
        const scope = document.querySelector(root);
        const nodes = scope ? [scope, ...scope.querySelectorAll("*")] : [];
        for (const node of nodes) {
          if (!node.getClientRects().length) continue;
          if (node.closest(".visually-hidden, script, style")) continue;
          const box = node.getBoundingClientRect();
          // A text field scrolls its own value by design.
          const field = node.matches("input, textarea, select");
          const scrolls = !field && node.clientWidth > 0 &&
            getComputedStyle(node).overflowX !== "visible" &&
            node.scrollWidth > node.clientWidth + 1;
          if (box.right > width + 1 || scrolls) {
            found.push({ element: node.tagName.toLowerCase(),
                         class: String(node.className).slice(0, 60),
                         text: (node.innerText || "").trim().slice(0, 40),
                         right: Math.round(box.right) });
          }
        }
        return found.slice(0, 8);
      })(arguments[0], arguments[1])
    JS
    assert_empty offenders,
                 "Horizontal overflow at #{width} px on #{page.current_path}"
  end

  # Every matching control is fully inside the viewport and at least 44 px
  # high and wide — measured without scrolling sideways.
  def assert_reachable_targets(width, selector)
    boxes = page.evaluate_script(<<~JS, selector)
      [...document.querySelectorAll(arguments[0])]
        .filter((node) => node.getClientRects().length)
        .map((node) => {
          const box = node.getBoundingClientRect();
          return { text: node.innerText.trim(), left: box.left,
                   right: box.right, width: box.width,
                   height: box.height };
        })
    JS
    assert_not_empty boxes, "No control matches #{selector}"
    boxes.each do |box|
      assert box["left"] >= 0 && box["right"] <= width + 1,
             "#{box['text']} is outside the #{width} px viewport: #{box}"
      assert_operator box["height"].round, :>=, 44, box["text"]
      assert_operator box["width"].round, :>=, 44, box["text"]
    end
  end
end
