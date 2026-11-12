---
title: Plugin reference
description: Reference for the Wopee.io Cypress plugin @wopee-io/wopee.cy. Configuration options, commands, element screenshots, ignore areas, failing on a visual difference, branches and CI.
type: Reference
updated: 12 November 2026
---

# Cypress plugin reference

Everything about `@wopee-io/wopee.cy` that [Getting started](01-getting-started.md) leaves out. Applies to version 4.13.6.

## Install

```shell
npm install -D @wopee-io/wopee.cy dotenv
```

Supported Cypress versions: 13 to 16. Cypress is a peer dependency: the plugin uses your project's Cypress and installs no copy of its own. Cypress 16 needs Node.js 22 or 24.

Version 4.12.2 and older support Cypress 13 and 14 only: on Cypress 15 and newer the spec fails to load with `Class extends value undefined is not a constructor or null`. They also install their own copy of Cypress 13, which downloads an extra Cypress binary during `npm install`. Update with `npm install -D @wopee-io/wopee.cy@latest`.

## Configuration

The plugin reads only the `wopee` object in the `env` section of the Cypress config. Register it with `addWopeePlugin(on, config)` in `setupNodeEvents` and the commands with `addWopeeCommands()` in the support file (see [Getting started](01-getting-started.md#4-register-the-plugin)).

```javascript
env: {
  wopee: {
    apiUrl: process.env.WOPEE_API_URL,
    apiKey: process.env.WOPEE_API_KEY,
    projectUuid: process.env.WOPEE_PROJECT_UUID,
    branchName: process.env.WOPEE_BRANCH_NAME,
  },
},
```

| Option | Required | Description |
| --- | --- | --- |
| `apiKey` | yes | API key from **More** › **Settings** › **API Keys** |
| `projectUuid` | yes | Project UUID from the same page |
| `apiUrl` | no | Default `https://api.wopee.io` |
| `branchName` | no | Branch of the run. Default `master`. |
| `baselineBranchName` | no | Branch to compare with when the current branch has no baseline yet |
| `pixelToPixelDiffTolerance` | no | Difference in percent that still counts as a match |
| `customTags`, `comment` | no | Free text stored with each step |
| `os`, `browser`, `device`, `viewport` | no | Labels that separate baselines per environment |
| `waitForAssets`, `waitForAssetsTimeout` | no | Defaults for every track, see [Wait for fonts and images](#wait-for-fonts-and-images) |
| `ignoreAreas` | no | CSS selectors left out of every step's comparison, see [Ignore areas](#ignore-areas) |
| `enableSoftAssert` | no | `false` fails the test when a step is `unresolved`. Default `true`. See [Fail the test on a visual difference](#fail-the-test-on-a-visual-difference). |

`WOPEE_*` variables that are not mapped into this object have no effect.

## Commands

| Command | Description |
| --- | --- |
| `cy.wopeeStartSuite(name)` | Starts a suite. Required before the first `cy.wopeeTrack()`. |
| `cy.wopeeStartScenario(name)` | Starts a scenario inside the suite. |
| `cy.wopeeTrack(options, responseCallback?, errorCallback?)` | Takes a screenshot and sends it for comparison. |
| `cy.wopeeStopScenario()` | Closes the scenario. |

`cy.wopeeTrack()` options:

| Option | Description |
| --- | --- |
| `stepName` | Required. Part of the baseline key `<scenario name>-<step name>`. |
| `comment`, `customTags`, `os`, `browser`, `device`, `viewport`, `pixelToPixelDiffTolerance`, `baselineBranchName` | Override the configuration for this one step (`os`, `browser` and `device` from 4.13.6) |
| `ignoreAreas` | Areas left out of this step's comparison, on top of the configuration's. See [Ignore areas](#ignore-areas). |
| `waitForAssets` | Wait for the page's web fonts and images before the screenshot. Default `true`. |
| `waitForAssetsTimeout` | How long that wait may take, in ms. Default `5000`. After that the screenshot is taken anyway. |
| `retryLimit` | How many times an `unresolved` step is tracked again. Default `0` since 4.13.4, so one attempt (4.13.3 and older: `2`). |
| Cypress screenshot options | For example `capture: "viewport"` |

The `responseCallback` receives `{ stepName, imageUrl, status }`:

```javascript
cy.wopeeTrack({ stepName: "Products" }, (result) => {
  cy.task("log", `${result.stepName}: ${result.status}`);
});
```

`cy.task("log")` needs a `log` task registered in `setupNodeEvents`.

### One element

Chain `cy.wopeeTrack()` after `cy.get()` to capture one element:

```javascript
cy.get(".inventory_list").wopeeTrack({ stepName: "Product list" });
```

### Wait for fonts and images

From 4.13.4, `cy.wopeeTrack()` loads every web font face and decodes every image of the page before it takes the screenshot, for up to `waitForAssetsTimeout` ms. A font or image that fails to load is skipped; one still loading at the timeout is written to the command log and the screenshot is taken anyway, so the test does not fail.

- Lazy images (`loading="lazy"`) outside the viewport and CSS background images are not awaited. Wait for such content with `cy.get(...).should("be.visible")` before the track.
- Set `waitForAssets` and `waitForAssetsTimeout` for every track in the `wopee` object, or for one step in `cy.wopeeTrack()`; the step option wins.
- 4.13.3 and older take the screenshot right away. Update the plugin, or wait for the fonts and images yourself as in [Wait for fonts and images before tracking](../visual-testing.md#wait-for-fonts-and-images-before-tracking).

### Ignore areas

Leave changing content, such as dates, ads or a live counter, out of the comparison. An entry of `ignoreAreas` is either:

- a **CSS selector**: covers every element it matches, measured right after the screenshot with a small margin around each. A selector that matches nothing on the page is skipped, so a banner that only some pages show does not fail the others.
- a **rectangle** `{ x, y, width, height }` in pixels of the screenshot.

```javascript
// cypress.config.js: for every step
env: { wopee: { /* ... */ ignoreAreas: [".cookie-banner", "[data-test=clock]"] } },

// a spec: for one step, on top of the configuration's
cy.wopeeTrack({
  stepName: "Checkout",
  ignoreAreas: [".delivery-date", { x: 0, y: 0, width: 300, height: 80 }],
});
```

Selectors work for full-page, viewport and element screenshots, with `padding` and `clip`. Ignore areas drawn in the Commander comparison view still apply on top.

4.13.5 and older do not send ignore areas, and fail the test when a selector matches nothing. Update the plugin.

### Fail the test on a visual difference

By default an `unresolved` step, one that differs from its approved baseline, passes the test and waits for review in **Runs**. Set `enableSoftAssert: false` in the `wopee` object to fail the test instead; the error names the step and links to it in Commander. With `retryLimit`, only the last attempt counts.

To let a step pass anyway, return `true` from the `errorCallback`, the third argument of `cy.wopeeTrack()`:

```javascript
cy.wopeeTrack({ stepName: "Products" }, undefined, (error) => {
  cy.task("log", error);
  return true; // the test goes on
});
```

4.13.5 and older never fail the test, whatever `enableSoftAssert` says. Update the plugin, or check `result.status` in the `responseCallback`.

## Branches and suites

- Baselines are kept per branch. Set `branchName` from your CI, for example `branchName: process.env.WOPEE_BRANCH_NAME` with `WOPEE_BRANCH_NAME=$GITHUB_REF_NAME`.
- A suite is identified by its name and branch: the same suite name on the same branch adds to the existing entry in **Runs**. Use a timestamp or build number in the suite name.
- See [Baselines and branches](../visual-testing.md#baselines-and-branches) for merging and managing baselines.

## Run in CI

Wopee.io works with any CI system. Set `WOPEE_PROJECT_UUID` and `WOPEE_API_KEY` as secrets of your CI (plus `WOPEE_API_URL` for a self-hosted instance) and run `npx cypress run` as usual. Cypress' own guides: [Continuous Integration](https://docs.cypress.io/guides/continuous-integration/introduction){: target="\_blank"}.

The repository Wopee.io creates for a Cypress project runs from Commander (**Runs** › **Start testing**), not on push; see [Template project › Run from Commander](02-template-project.md#run-from-commander).
