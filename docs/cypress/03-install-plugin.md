---
title: Install Plugin
---

To start visual testing with your existing Cypress tests, leverage the benefits of the Wopee.io Cypress plugin. Follow the steps below to install the plugin.

## Prerequisites

- Visual Studio Code or any other code editor
- Wopee.io [account](https://cmd.wopee.io)

## Environment setup

### Set Wopee.io API key

Before running the visual test, set up your API key as an environment variable named `WOPEE_API_KEY`.
You may set it from the command line like this:

=== "Linux/MacOS"

    ```shell
    export WOPEE_API_KEY=your-api-key
    ```

=== "Windows"

    ```shell
    set WOPEE_API_KEY=your-api-key
    ```

### Set `.env` file params

You need to set your own `.env` file to your project.

This is a sample `.env` file:

```shell
# Mandatory
WOPEE_API_URL=https://api.wopee.io/
WOPEE_PROJECT_UUID=your-project-uuid


```

Full list of `.env` file parameters could be found [here](https://docs.wopee.io).

??? tip "Where to find project UUID and Wopee.io API key?"

    You can find your project UUID and Wopee.io API key in the project settings screen after navigating to project.

    ![Project UUID](/img/project-settings.gif)

### Set up CI/CD

!!! tip

    Wopee.io support visual testing with all modern Continuous Integration (CI) providers and systems. When you run your tests in CI, you can set up your environment variables in the CI system settings.

    For Cypress, you need find more information about it in the [Cypress documentation](https://docs.cypress.io/guides/guides/continuous-integration.html#Setting-up-CI) and [CI Provider Examples](https://docs.cypress.io/guides/continuous-integration/ci-provider-examples).

### Enhance Cypress configuration

Configuration of Cypress is done in `cypress.config.ts` file. Add the following configuration to the file:

```javascript
import "dotenv/config";
import { addWopeePlugin } from '@wopee-io/wopee.cy';

// . . . OR in case of CommonJS
// const dotenv = require('dotenv')
// const { addWopeePlugin } = require("@wopee-io/wopee.cy");
// require("dotenv").config();

...

export default defineConfig({
  ...
  env: {
    wopee: {
      apiUrl: process.env.WOPEE_API_URL,
      apiKey: process.env.WOPEE_API_KEY,
      projectUuid: process.env.WOPEE_PROJECT_UUID,
    },
  },
  ...
  e2e: {
    setupNodeEvents(on, config) {
      addWopeePlugin(on, config);
    },
  },
});
```

## Add Wopee.io plugin (as custom commands)

```javascript
// cypress/support/commands.js

import { addWopeeCommands } from '@wopee-io/wopee.cy'
addWopeeCommands()
```

## Install dependencies

Install all dependencies:

    npm i -D @wopee-io/wopee.cy
    npm i -D dotenv

## Sample test

To run sample test create a new file `cypress/integration/wopee.spec.js` with the following content:

```javascript
/// <reference types="cypress" />
/// <reference types="@wopee-io/wopee.cy" />

// const testSuiteName = "cy-wopee-io integration - 1st-run";
const testSuiteName = 'cy-wopee-io integration - regression'

describe(testSuiteName, () => {
  before(() => {
    cy.wopeeStartSuite(testSuiteName)
  })

  beforeEach(() => {
    cy.wopeeStartScenario(Cypress.currentTest.title)
  })

  afterEach(() => {
    cy.wopeeStopScenario()
  })

  it('Correct login - minimalistic', () => {
    cy.visit('https://dronjo.wopee.io/')
    cy.get('#sign_in').click()

    cy.get('input[name="user"]').type('marcel.veselka@tesena.com')
    cy.get('input[name="password"]').type('admin')

    cy.get('button').contains('sign in').click()

    // Autonomous (low-code) assert: Wopee visual check
    cy.wopeeTrack({ stepName: 'User is logged in' })
  })
})
```

## Run tests

Run first demo test:

    npx cypress run --spec cypress/integration/wopee.spec.js
