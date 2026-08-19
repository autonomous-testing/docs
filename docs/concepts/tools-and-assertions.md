---
title: Tools & Assertions
description: How Wopee.io agents interact with your app using click, type, select tools and validate outcomes with assertions. Generates plain Playwright code.
---

# Tools & Assertions (Wopee.io)

## What this page covers

How the agent interacts with your app, how it validates outcomes, and how locators are chosen. After a scenario runs, Wopee.io generates **plain test code** (e.g., Playwright) that you can run anywhere, **no LLMs or Wopee.io runtime required**.

---

## Execution flow (at a glance)

1. **Select interaction tool** (click, type, select, etc.) for the desired action.
2. **Agent automatically chooses locator strategy** (ARIA/HTML/visual) based on the tool and target element.
3. **Perform interactions** using the selected tool and optimal locator.
4. **Validate results** with assertions (text, visibility, URL, visual).
5. **Export deterministic code** that mirrors the exact tools and locators used.

---

## Interaction tools

Use these to drive the UI.
_(Tip: prefer semantic/accessible targets first; fall back to visual only when needed.)_

- **Click** – Click an element once. Double-click and right-click variants are available.
- **Visual click** – Click by visual position (e.g., canvas elements or icons without a stable DOM locator). Positions can be viewport percentages, so they survive resolution changes.
- **Fill** – Set the value of an input/textarea in one step. The default for text input.
- **Type** – Type character by character, for type-ahead and autocomplete fields that only show suggestions on real keystrokes. Replaces the current field content.
- **Select** – Choose an option in a `<select>` or custom dropdown.
- **Hover** – Move the pointer over an element (tooltips/menus).
- **Press** – Send keyboard keys or combos (e.g., `Enter`, `Ctrl+S`), optionally holding a key for a set duration (useful for games and canvas apps).
- **Scroll** – Scroll the page or a specific container: up/down, by pixels, or to top/bottom.
- **Resize viewport** – Change the browser viewport size mid-test (e.g., `1024x768`).
- **Navigate to URL** – Open a specific URL or path.
- **HTTP request** – Call an API directly from a test step (GET/POST/PUT/PATCH/DELETE and more). See the [HTTP Request Tool guide](../guides/http-tools.md).
- **Add cookie** – Set a cookie (auth/session/bootstrap).
- **Upload file** – Attach a file to a file input. Files are read from your project's `data/` directory (see [Upload files](../guides/upload-files.md)).
- **Wait** – Pause for a bounded time. Prefer a poll assert that waits for a condition instead of a fixed sleep.

**Tool-locator relationship**

The tool you select influences how the agent chooses locators:

- **Standard tools** (Click, Fill, Select) → Agent prefers ARIA/HTML locators
- **Visual tools** (Visual click, Visual assert) → Agent automatically uses visual location strategies
- **Navigation tools** (Navigate to URL) → No locator needed
- **System tools** (Add cookie, Upload file) → Agent finds the appropriate input elements using DOM locators

## Assertion tools

Use these to prove the UI is in the expected state.

- **Verify visibility** – Assert that an element is rendered and visible, or that it is not. When you expect an element to be gone, its absence from the page counts as a pass.
- **Contain text** – Assert an element's text contains a string or regex. Plain strings match case-insensitively, `a|b|c` alternation is supported, and form fields (inputs, dropdowns) are checked by their value.
- **URL assert** – Assert the current page URL contains a string or matches a regex. Useful for verifying redirects and navigation outcomes.
- **Visual assert** – LLM-assisted visual check written in natural language, e.g.,
  "**Shopping cart shows a badge with 4 items**." The result carries a confidence score and the value the agent actually observed on screen.
  _Great for UI semantics that are hard to express via raw locators; avoid for pixel-perfect needs, use DOM/text assertions instead when possible._
- **Poll assert** – Repeat any of the above until it passes or a deadline is reached (up to 4 minutes). Use it to wait for slow transitions, background jobs, or data that takes time to appear.

!!! tip "Never assert values that change between runs"

    A passing assertion is saved as an expectation for future runs. Do not assert literal balances, totals, timestamps, or order numbers; they will differ on the next run and fail it. Use a test variable, a regex for the format (e.g., `/€\d+\.\d{2}/`), or a visual assert question instead.

---

## Custom tool

Provide a short instruction (natural language). The agent will **choose the right tool automatically**, **select the optimal locator strategy** for each element, and Wopee.io will **translate it into explicit steps** in the generated code.
_Example:_ "Open settings and enable dark mode" → navigate, click toggles, and assert theme change.

!!! note "When to use custom tools"

    **Use specific tools when possible**: The more specific you are with tool selection, the more stable and predictable the execution will be. Custom tools are helpful for agent experimentation and fine-tuning behavior, but should only be used when there isn't a specific tool available for your needs.

---

## Locator strategies (automatic selection)

The agent automatically selects the optimal locator strategy based on the tool you choose and the target element:

1. **ARIA tree (preferred)** – Role/name-based locators from accessible markup (stable and intent-focused).
2. **HTML attributes** – IDs, data-test IDs, classes, and CSS/XPath (use data-test IDs for stability).
3. **Visual location** – x, y or image heuristics (last resort for canvas, icons without DOM hooks, etc.).

**How it works**

- **Tool-driven selection**: When you choose a tool (e.g., "Click"), the agent analyzes the target element and automatically picks the best locator strategy.
- **Fallback logic**: If the preferred strategy fails, the agent automatically tries the next best option.
- **Code generation**: The selected locator strategy is directly used in the generated test code.

**Guidance**

- The agent aims for **stable, readable locators**, in the same order as above: ARIA role/name first, then data-test IDs and other HTML attributes, visual position last.
- **Visual tools** (like "Visual click") automatically trigger visual location strategies.
- Keep assertions **specific and minimal**: verify what proves the behavior, not everything on the page.

---

## Code generation

After a successful agent run, Wopee.io emits **deterministic test code** that exactly mirrors the tools you selected and the locator strategies the agent automatically chose. The generated code uses the same interaction tools and locators that were used during the agent's execution, ensuring consistency between what the agent did and what your tests will do. You can commit this code to your repo and run it in CI/CD without Wopee.io or LLMs.

---

## Example (concise)

1. Navigate to `/cart`
2. Click **Checkout**
3. Fill **Email** = `alice@example.com`
4. Press **Enter**
5. **Verify visibility** of **Order summary**
6. **Contain text** on **Total** matches `/€\d+\.\d{2}/`

---

## Good practices

!!! tip "Tools & Assertions best practices"

    - **Trust the agent's locator selection**: The agent automatically chooses the best locator strategy based on your tool selection
    - **Use data-test IDs**: Add stable identifiers to your elements for reliable testing (the agent will prefer these)
    - **Keep assertions focused**: Verify only what proves the behavior, not everything on the page
    - **Reserve visual tools**: Use visual clicks/asserts only when DOM selection isn't possible
    - **Write clear custom instructions**: Be specific about what you want the agent to accomplish
    - **Let the agent handle complexity**: Focus on what you want to test, not how to locate elements
    - **Configure interaction rules**: Use project context, code examples, and code rules to specify preferred interaction and assertion patterns

!!! note "Advanced configuration options"

    You can customize interaction and assertion behavior using:

    - **Project context** (all plans): Define application-specific rules and preferences
    - **Code examples** (Enterprise & Premium): Provide sample code patterns for the agent to follow
    - **Code rules** (Enterprise & Premium): Set specific coding standards and conventions

    These features help ensure consistent tool usage and code generation across your test suite.

## Related topics

- [Getting Started with Wopee.io Agent testing](../ai-agent.md)
- [Self-Healing](self-healing.md)
- [Analysis Process](analysis-process.md)
- [Prompting Guidelines](prompting-guidelines.md)
- [Project Context](../guides/project-context.md)
- [HTTP Request Tool](../guides/http-tools.md)
