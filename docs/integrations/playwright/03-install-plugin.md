---
title: Install Plugin
---

To start visual testing with your existing Playwright tests, leverage the benefits of the Wopee.io. Follow the steps below to install the plugin.

## Prerequisites

- [Node.js](https://nodejs.org/en/download/)
- Visual Studio Code or any other code editor
- Playwright project set up (if you don't have one, follow the [Playwright Getting Started](https://playwright.dev/docs/intro){: target="\_blank"} guide)
- Wopee.io [free account](https://cmd.wopee.io){: target="\_blank"}

## Create a new Playwright project

1. Navigate to Wopee.io [project page](https://cmd.wopee.io/projects) and click `New Integration` button `Playwright`.
   ![New project button](/img/new-project.png)

2. Fill in the project name, url and click `Create`.
   ![New project form](/img/new-project-form.png)

## Environment setup (API key, project UUID)

??? tip "Where to find project UUID and Wopee.io API key?"

    You can find your project UUID and Wopee.io API key in the project settings screen after navigating to project.

    ![Project UUID](/img/project-settings.gif)

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
WOPEE_PROJECT_UUID=your-project-uuid
```

Full list of `.env` file parameters could be found [here](https://docs.wopee.io).

## Install dependencies

Install all dependencies:

    npm i -D @wopee-io/wopee.pw

## Sample tests

### Minimal test

To run sample test create a new file `tests/mini.spec.ts` and paste the following code:

```typescript
import { Wopee } from '@wopee-io/wopee.pw'
import { test } from '@playwright/test'

test.describe('test', () => {
  let wopee: Wopee
  test.beforeAll(async () => {
    wopee = new Wopee()
    await wopee.startSuite('Minimal example')
  })

  test.afterEach(async () => {
    await wopee.stopScenario()
  })

  test('test', async ({ page }) => {
    await page.goto('https://playwright.dev/')

    const screenshot = await page.screenshot()
    const imageBase64 = screenshot.toString('base64')
    await wopee.trackImage({
      stepName: 'image',
      scenarioName: 'test',
      imageBase64: imageBase64,
    })
  })
})
```

### More complex test

To run sample test create a new file `tests/wopee.spec.ts` and paste the following code:

```typescript
import { Wopee } from '@wopee-io/wopee.pw'
import { test } from '@playwright/test'

test.describe('test', () => {
  let wopee: Wopee
  test.beforeAll(async () => {
    wopee = new Wopee()

    const now = new Date()
    const date = `${now.getDate().toString().padStart(2, '0')}-${(now.getMonth() + 1).toString().padStart(2, '0')}-${now.getFullYear()}`
    await wopee.startSuite(`test-${date}`)
  })

  test.afterEach(async () => {
    await wopee.stopScenario()
  })

  test('trackImage', async ({ page }) => {
    await page.goto('https://playwright.dev/')

    const screenshot = await page.screenshot({ type: 'png' })
    const imageBase64 = screenshot.toString('base64')

    await wopee.trackImage({
      comment: 'comment',
      customTags: 'customTags',
      imageBase64: imageBase64,
      pixelToPixelDiffTolerance: 1.0,
      scenarioName: 'trackImageWithoutStartScenario',
      stepName: 'image-trackImage',
      viewport: 'viewport',
    })
  })

  test('trackFullPageScreenshot', async ({ page }) => {
    await page.goto('https://playwright.dev/')

    await wopee.trackFullPage({
      comment: 'comment',
      customTags: 'customTags',
      page: page,
      pixelToPixelDiffTolerance: 1.0,
      scenarioName: 'trackFullPageScreenshotWithoutStartScenario',
      stepName: 'image-trackFullPageScreenshot',
      viewport: 'viewport',
    })
  })

  test('trackElement', async ({ page }) => {
    await page.goto('https://playwright.dev/')

    const element = page.locator('//a[@class="getStarted_Sjon"]')

    await wopee.trackElement({
      comment: 'comment',
      customTags: 'customTags',
      locator: element,
      pixelToPixelDiffTolerance: 1.0,
      scenarioName: 'trackElementWithoutStartScenario',
      stepName: 'element',
      viewport: 'viewport',
    })
  })

  test('trackViewport', async ({ page }) => {
    await page.goto('https://playwright.dev/')

    const element = page.locator('//a[@class="getStarted_Sjon"]')

    await wopee.trackElement({
      comment: 'comment',
      customTags: 'customTags',
      locator: element,
      pixelToPixelDiffTolerance: 1.0,
      scenarioName: 'trackViewportWithoutStartScenario',
      stepName: 'viewport',
      viewport: 'viewport',
    })
  })
})
```

## Run tests

Run first demo test:

    npx playwright test tests/mini.spec.ts

OR

    npx playwright test tests/wopee.spec.ts
