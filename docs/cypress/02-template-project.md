---
title: Template project
description: Start Wopee.io visual testing with the Cypress template project. Configure your project UUID and API key and run the sample test.
---

# Cypress template project

The [Cypress template project](https://github.com/Wopee-io/cypress-template){: target="\_blank"} is a ready Cypress setup with the Wopee.io plugin and a sample test. It uses Cypress 13 and the same plugin setup as [Getting started](01-getting-started.md).

## Prerequisites

- [Node.js](https://nodejs.org/en/download/){: target="\_blank"} 18 or newer
- A Wopee.io project with the test framework **Cypress** and an API key: follow steps 1 and 2 of [Getting started](01-getting-started.md)

## Get the template project

```shell
git clone https://github.com/Wopee-io/cypress-template
cd cypress-template
npm install
```

## Configure the environment

Copy `.env.example` to `.env` and fill in your values:

```shell
WOPEE_API_URL=https://api.wopee.io
WOPEE_PROJECT_UUID=your-project-uuid
WOPEE_API_KEY=your-api-key
```

`.env.example` also lists `WOPEE_PROJECT_URL` and `WOPEE_CI_BUILD_ID`; the plugin does not read them. The template maps the `WOPEE_*` variables into the `env.wopee` object in `cypress.config.ts`, as described in [Getting started › Register the plugin](01-getting-started.md#4-register-the-plugin).

The sample test opens `baseUrl` from `cypress.config.ts`. Change it to your application URL and adjust the test to your pages. Add `cy.pageReady()` before each `cy.wopeeTrack()` as shown in [Wait until the page is ready](01-getting-started.md#6-wait-until-the-page-is-ready).

Do not commit `.env`.

## Run the sample test

```shell
npm test
```

This runs `cypress/e2e/simple.spec.cy.ts`. The terminal prints one `[wopee]: Tracking response:` line per tracked step, with its status and a link to the step in Commander.

## Review the results

Open **Runs** in Commander and select the run. On the first run every step is `new`: open each step and click **Approve** to make it the baseline. On the next run, matching steps are `ok` and changed steps are `unresolved`. See [Getting started › Approve in Runs](01-getting-started.md#9-approve-in-runs).

![Comparison view with a new step and the Approve button](../img/visual-testing/runs-comparison.webp)
