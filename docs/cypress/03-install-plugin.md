---
title: Plugin reference
description: Reference for the Wopee.io Cypress plugin @wopee-io/wopee.cy. Configuration options, commands, element screenshots, branches, CI and known issues.
---

# Cypress plugin reference

Everything about `@wopee-io/wopee.cy` that [Getting started](01-getting-started.md) leaves out. Applies to version 4.12.2.

## Install

```shell
npm install -D @wopee-io/wopee.cy dotenv
```

Supported Cypress versions: 13 and 14. With Cypress 15 and newer the spec fails to load with `Class extends value undefined is not a constructor or null`; pin `cypress@14.5.4` until a fixed plugin version is released. The plugin also installs its own copy of Cypress 13 as a dependency, which downloads an extra Cypress binary during `npm install`.

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

`WOPEE_*` variables that are not mapped into this object have no effect.

## Commands

| Command | Description |
| --- | --- |
| `cy.wopeeStartSuite(name)` | Starts a suite. Required before the first `cy.wopeeTrack()`. |
| `cy.wopeeStartScenario(name)` | Starts a scenario inside the suite. |
| `cy.wopeeTrack(options, responseCallback?)` | Takes a screenshot and sends it for comparison. |
| `cy.wopeeStopScenario()` | Closes the scenario. |

`cy.wopeeTrack()` options:

| Option | Description |
| --- | --- |
| `stepName` | Required. Part of the baseline key `<scenario name>-<step name>`. |
| `comment`, `customTags`, `viewport`, `pixelToPixelDiffTolerance`, `baselineBranchName` | Override the configuration for this one step |
| `retryLimit` | How many times an `unresolved` step is tracked again. Default `2`, so up to three attempts. Set `0` to track once. |
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

Cypress screenshots right away. Call `cy.pageReady()` from [Getting started › Wait until the page is ready](01-getting-started.md#6-wait-until-the-page-is-ready) before every track.

## Branches and suites

- Baselines are kept per branch. Set `branchName` from your CI, for example `branchName: process.env.WOPEE_BRANCH_NAME` with `WOPEE_BRANCH_NAME=$GITHUB_REF_NAME`.
- A suite is identified by its name and branch: the same suite name on the same branch adds to the existing entry in **Runs**. Use a timestamp or build number in the suite name.
- See [Baselines and branches](../visual-testing.md#baselines-and-branches) for merging and managing baselines.

## Run in CI

Wopee.io works with any CI system. Set `WOPEE_API_URL`, `WOPEE_PROJECT_UUID` and `WOPEE_API_KEY` as secrets of your CI and run `npx cypress run` as usual. Cypress' own guides: [Continuous Integration](https://docs.cypress.io/guides/continuous-integration/introduction){: target="\_blank"}.

## Known issues in 4.12.2

- Cypress 15 and newer are not supported (see [Install](#install)).
- An `unresolved` step never fails the test, also with `enableSoftAssert` set. Use the `responseCallback` to act on the status.
- Ignore areas passed to `cy.wopeeTrack()` are not sent. Draw ignore areas in the Commander comparison view instead.
- The npm README Quick Start is outdated: it uses flat `WOPEE_*` keys in `cypress.env.json` and `cy.wopeeTrack('name')`. Use the setup on this page.
