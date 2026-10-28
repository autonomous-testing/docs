---
description: Add Wopee.io visual testing to your WebdriverIO tests. Install the @wopee-io/wopee.wdio service, add track commands, review differences in Commander, or start from the template project.
---

# WebdriverIO

Add visual checks to your existing WebdriverIO tests with the `@wopee-io/wopee.wdio` service. Each `browser.track...()` command sends a screenshot to Wopee.io, which compares it with the approved baseline. You review the differences in Commander and approve or reject them.

This page walks through a complete example on [Sauce Demo](https://www.saucedemo.com){: target="\_blank"}: two screenshots, a first run that creates the baselines, and a second run that catches a visual bug. Verified with `@wopee-io/wopee.wdio` 6.0.0 and WebdriverIO 9 (Mocha, Chrome). Prefer a ready project? Start from the [template project](#template-project).

## Prerequisites

- Node.js 20 or newer
- WebdriverIO 9 (or 8) with a test framework such as Mocha. `npm init wdio` sets one up.
- Google Chrome. WebdriverIO 9 downloads the matching ChromeDriver on the first run.
- A Wopee.io account at [cmd.wopee.io](https://cmd.wopee.io){: target="\_blank"}

## 1. Create a project

1. In Commander, click **NEW PROJECT** and paste the **App URL** (for example `https://www.saucedemo.com`).
2. Open **Advanced settings** and set **Test framework** to **WebdriverIO**. **Explore the app and generate tests** switches off, because test generation is available for Playwright only.
3. Click **Create project**.

![Test framework picker in the New project dialog](img/visual-testing/new-project-framework.webp){ width="440" height="520" }

## 2. Get the API key

1. In the project, open **More** › **Settings** › **API Keys** and copy `WOPEE_PROJECT_UUID`.
2. Enter a name, click **Generate a new key** and copy `WOPEE_API_KEY`. The key is shown **only once**.

![API Keys in project settings](img/visual-testing/api-keys.webp){ width="600" height="433" loading="lazy" }

## 3. Install

```shell
npm install --save-dev @wopee-io/wopee.wdio dotenv
```

`webdriverio` is a peer dependency; projects created with `npm init wdio` already have it.

Create a `.env` file in the project root:

```shell
WOPEE_PROJECT_UUID=your-project-uuid
WOPEE_API_KEY=your-api-key
```

`WOPEE_API_URL` is needed only for a self-hosted instance (its URL is shown in **API Keys**); the service defaults to `https://api.wopee.io`. Add `.env` to `.gitignore`. In CI, set the same variables as secrets.

## 4. Configure the service

Load `.env` and add the service to `wdio.conf.ts`:

```typescript title="wdio.conf.ts"
import 'dotenv/config';

export const config: WebdriverIO.Config = {
  // ...your runner, specs, capabilities, framework and reporters
  services: [
    [
      '@wopee-io/wopee.wdio',
      {
        screenshotValidation: {
          apiUrl: process.env.WOPEE_API_URL,
          apiKey: process.env.WOPEE_API_KEY,
          projectUuid: process.env.WOPEE_PROJECT_UUID,
        },
        isLandscape: false,
      },
    ],
  ],
};
```

- The connection settings go **inside** `screenshotValidation`. The service does not pick up `WOPEE_*` variables on its own; pass every value through the config.
- `isLandscape` sits **next to** `screenshotValidation`. Set it to `false` for desktop browsers: the default `true` is meant for mobile devices in landscape orientation and crops desktop screenshots to the wrong size.

For TypeScript, add the service types to `tsconfig.json` so `browser.trackScreen()` and the other commands are typed:

```json title="tsconfig.json"
{
  "compilerOptions": {
    "types": ["node", "@wdio/globals/types", "@wopee-io/wopee.wdio"]
  }
}
```

## 5. Track screenshots in your test

```typescript title="test/specs/saucedemo.visual.ts"
import { browser, $ } from '@wdio/globals';

const user = process.env.SAUCE_USER ?? 'standard_user';

describe('Sauce Demo', () => {
  before(async () => {
    await browser.startSuite(`WebdriverIO demo ${new Date().toISOString().slice(0, 16)}`);
  });

  it('logs in and shows the products', async () => {
    await browser.startScenario('WebdriverIO: login and products');

    await browser.url('https://www.saucedemo.com');
    await $('#login-button').waitForDisplayed();
    await browser.execute(async () => {
      await document.fonts.ready;
    });
    const login = await browser.trackScreen({ stepName: 'Login page' });
    console.log('Login page:', login.screenshotValidationResult);

    await $('#user-name').setValue(user);
    await $('#password').setValue('secret_sauce');
    await $('#login-button').click();
    await $('.inventory_list').waitForDisplayed();
    await browser.execute(async () => {
      await Promise.all([...document.images].map((img) => img.decode().catch(() => {})));
    });

    const products = await browser.trackScreen({ stepName: 'Products' });
    console.log('Products:', products.screenshotValidationResult);

    await browser.stopScenario();
  });
});
```

| Command | Purpose |
| --- | --- |
| `browser.startSuite(name)` | Starts a suite (one entry in **Runs**). Call it once, in `before`. A suite with the same name and branch is reused, so the timestamp gives every run its own entry. |
| `browser.startScenario(name)` | Starts a scenario. Use a stable name; it is part of the baseline key. |
| `browser.trackScreen({ stepName })` | Takes a screenshot of the visible part of the page and compares it with the baseline. |
| `browser.stopScenario()` | Closes the scenario. |

The two `browser.execute()` calls wait for web fonts and for every image to decode before tracking. See [Wait for fonts and images before tracking](visual-testing.md#wait-for-fonts-and-images-before-tracking).

Other track commands:

| Command | Captures |
| --- | --- |
| `browser.trackFullPageScreen({ stepName })` | The whole page, scrolled and stitched |
| `browser.trackElement({ stepName, element })` | One element. In WebdriverIO 9 pass `await $('selector').getElement()`. |
| `browser.trackImage({ stepName, imageBase64 })` | Any PNG you provide as base64, for example from `browser.takeScreenshot()` |

There is no `wopeeTrack` command in WebdriverIO. All track commands accept the optional `comment`, `customTags`, `pixelToPixelDiffTolerance`, `viewport` and `baselineBranchName`, and return `{ screenshotValidationResult: { stepName, imageUrl, status } }`.

## 6. First run: create the baselines

```shell
npx wdio run wdio.conf.ts
```

```text
[0-0] Login page: {
[0-0]   stepName: 'Login page',
[0-0]   imageUrl: 'https://cmd.wopee.io/tests?projectId=...&suiteId=...&stepId=...&tab=RUNS',
[0-0]   status: 'new'
[0-0] }
[0-0] Products: {
[0-0]   stepName: 'Products',
[0-0]   imageUrl: 'https://cmd.wopee.io/tests?projectId=...&suiteId=...&stepId=...&tab=RUNS',
[0-0]   status: 'new'
[0-0] }
[0-0] PASSED in chrome - file:///test/specs/saucedemo.visual.ts
```

Both steps are `new`: there is no baseline yet. Add `--logLevel info` to see when the suite and scenario start and stop.

## 7. Approve in Runs

Open the project and go to **Runs**. Select the run `WebdriverIO demo ...`, then each step, and click **Approve**. The screenshot becomes the baseline.

![Comparison view with a new step and the Approve button](img/visual-testing/runs-comparison.webp){ width="1600" height="775" loading="lazy" }

## 8. Second run: catch a visual bug

Sauce Demo has a `visual_user` whose products page is visually broken. Run the same test as that user:

```shell
SAUCE_USER=visual_user npx wdio run wdio.conf.ts
```

```text
[0-0] Login page: {
[0-0]   stepName: 'Login page',
[0-0]   imageUrl: 'https://cmd.wopee.io/tests?projectId=...&suiteId=...&stepId=...&tab=RUNS',
[0-0]   status: 'ok'
[0-0] }
[0-0] Products: {
[0-0]   stepName: 'Products',
[0-0]   imageUrl: 'https://cmd.wopee.io/tests?projectId=...&suiteId=...&stepId=...&tab=RUNS',
[0-0]   status: 'unresolved'
[0-0] }
[0-0] PASSED in chrome - file:///test/specs/saucedemo.visual.ts
```

**Login page** matches the baseline. **Products** is `unresolved`: open it in **Runs**, inspect the highlighted differences and **Reject** it as a bug, or **Approve** it if the change is intended.

![Unresolved step with the difference overlay next to the baseline](img/visual-testing/runs-diff.webp){ width="1600" height="775" loading="lazy" }

## Good to know

- **A difference does not fail the test.** The test passes and the step waits for review. To fail the test as well, check the returned status:

    ```typescript
    const products = await browser.trackScreen({ stepName: 'Products' });
    expect(products.screenshotValidationResult?.status).not.toBe('unresolved');
    ```

- **Baselines** are identified by `<scenario name>-<step name>` plus the branch and the environment labels. Keep both names stable between runs.
- **Branches**: set `branchName` in `screenshotValidation` (default `master`). See [Branches in CI](#branches-in-ci) and [Baselines and branches](visual-testing.md#baselines-and-branches).
- **Statuses**: `new`, `ok`, `unresolved`, `autoApproved`. See [How it works](visual-testing.md#how-it-works).

## Configuration

Options inside `screenshotValidation`:

| Option | Default | Description |
| --- | --- | --- |
| `apiKey` | required | API key from **More** › **Settings** › **API Keys** |
| `projectUuid` | required | Project UUID from the same page |
| `apiUrl` | `https://api.wopee.io` | API endpoint. Set it only for a self-hosted instance (its URL is shown in **API Keys**). |
| `branchName` | `master` | Branch the screenshots belong to |
| `baselineBranchName` | | Branch to compare with when the current branch has no baseline yet |
| `pixelToPixelDiffTolerance` | `0` | Difference in percent that still counts as a match |
| `customTags`, `comment` | | Stored with each step |
| `browser`, `device`, `os`, `viewport` | | Labels that are part of the baseline identity |
| `screenshotValidationEnabled` | `true` | `false` runs the tests without sending screenshots |

Options next to `screenshotValidation`:

| Option | Default | Description |
| --- | --- | --- |
| `isLandscape` | `true` | Set to `false` for desktop browsers |
| `imageProcessing` | `mode: 'none'` | `mode: 'masking'` or `'cropping'` with `xLeft`, `xRight`, `yTop`, `yBottom` and `maskColor` to hide or cut screen edges on every screenshot |

### Branches in CI

```typescript
screenshotValidation: {
  apiUrl: process.env.WOPEE_API_URL,
  apiKey: process.env.WOPEE_API_KEY,
  projectUuid: process.env.WOPEE_PROJECT_UUID,
  branchName: process.env.WOPEE_BRANCH_NAME ?? 'master',
  baselineBranchName: process.env.WOPEE_BASELINE_BRANCH_NAME,
},
```

The repository Wopee.io creates for a WebdriverIO project runs from Commander (**Runs** › **Start testing**), not on push; see [Run from Commander](#run-from-commander).

## Template project

When you create a project with the test framework **WebdriverIO**, Wopee.io creates a repository for it from the [WebdriverIO template](https://github.com/Wopee-io/webdriverio-template){: target="\_blank"} and fills in your project settings. It is a ready WebdriverIO 9 setup (Mocha, headless Chrome) with the service configured as above and one sample test.

| File | What it does |
| --- | --- |
| `wdio.conf.ts` | Registers the service with the `screenshotValidation` block and `isLandscape: false`. `baseUrl` is `WOPEE_PROJECT_URL`, the App URL of your project. |
| `tests/example.spec.ts` | The sample test: opens your app at 1920x1080 and tracks three steps, `fullPage` (`trackFullPageScreen`), `screen` (`trackScreen`) and `image` (`trackImage`). |
| `.env.example` | Your project's values for local runs. Only `WOPEE_API_KEY` is empty. |
| `.github/workflows/tests.yml` | The workflow Commander starts. |

### Run from Commander

Nothing to set up. In Commander open **Runs** › **Start testing**. Commander runs the repository's tests in GitHub Actions with your project settings and shows the results under **Runs**.

The workflow has no manual **Run workflow** button in GitHub and does not run on push. To run the tests on every push or pull request, add your own trigger to `.github/workflows/tests.yml`.

### Run locally

Needs Node.js 20 or newer, git and Google Chrome.

```shell
git clone <your project's repository>
cd <repository folder>
cp .env.example .env
```

Open `.env` and paste an API key after `WOPEE_API_KEY=`. Create the key in Commander › **More** › **Settings** › **API Keys**; it is shown only once (see [Get the API key](visual-testing.md#2-get-the-api-key)). The other values are already your project's. `.env` is in `.gitignore`; do not commit it.

```shell
npm ci
npm test
```

The console prints a `Tracking response` line for each tracked step, with its status and a link to the step in Commander. `WOPEE_API_URL` stays commented out for [cmd.wopee.io](https://cmd.wopee.io){: target="\_blank"}; set it only for a self-hosted instance.

### Review the results

Open **Runs** in Commander and select the suite **service browsers-** followed by the date and time of the run. The sample puts the date and time into the suite name, so every run is its own entry.

- First run: the steps `fullPage`, `screen` and `image` are `new`. Check the screenshots and click **Approve**; they become the baselines.
- Next runs: a step is `ok` when the page looks the same, or `unresolved` when it differs. Open it, then **Approve** it as the new baseline or **Reject** it as a bug.

A visual difference is reported in Commander; it does not fail the WebdriverIO test. See [Review in Runs](visual-testing.md#3-review-in-runs).

### Local runs and Commander baselines

Compare like with like. A screenshot from your machine differs from one taken by Commander's runner: screen scaling and font rendering are not the same, for example on a Mac. A local run against a baseline approved from Commander is therefore `unresolved`. Keep the baselines from one place, usually Commander, and do not approve local screenshots over them.

For small rendering differences between runs on the same machine, set `WOPEE_PIXEL_TO_PIXEL_DIFF_TOLERANCE` in `.env`: the difference in percent that still counts as a match. The template already maps it to `pixelToPixelDiffTolerance`.

### Make it yours

- **Your app:** `browser.url('/')` opens `baseUrl`, which is `WOPEE_PROJECT_URL`. For local runs change it in `.env`; for runs from Commander change the App URL of the project in Commander.
- **More checks:** add `await browser.trackScreen({ stepName: 'Inventory page' })` after an interaction. Every `stepName` gets its own baseline. See [Other track commands](#5-track-screenshots-in-your-test) for full page, element and image.
- **More tests:** add `*.spec.ts` files under `tests/` and list them in `specs` in `wdio.conf.ts`. Every test needs what the sample has: start a suite and a scenario, track, stop the scenario.
- **Desktop screenshots:** keep `isLandscape: false`; `true` is for mobile devices in landscape and rotates desktop screenshots.

### Cloned the public template?

If `.env` contains `put-your-project-uuid-here`, you cloned the public template, not your project's repository. Put in your project UUID from **More** › **Settings** › **API Keys** (`WOPEE_PROJECT_UUID`) and your app's URL (`WOPEE_PROJECT_URL`), then run as in [Run locally](#run-locally).

## Troubleshooting

| Message | Fix |
| --- | --- |
| `Failed to initialise service @wopee-io/wopee.wdio` naming `apiKey` or `projectUuid` | The value is missing. Check `.env`, that `wdio.conf.ts` starts with `import 'dotenv/config'`, and that the values are inside `screenshotValidation`. |
| `must be an absolute URL including the scheme` | Write `apiUrl` with `https://`. |
| `ZodError ... Expected object, received null` or an authorization error | The API key usually belongs to another Wopee.io instance or another project. Create the key in the Commander you run against. Set `WOPEE_API_URL` only for a self-hosted instance. |
| `Error: Unsupported type: function` from `trackElement` | The selector matched nothing on the page. Use a selector from your app. |
| `browser.trackScreen is not a function` | The service is not listed in `services`, or the package is not installed. |
| The screenshot is narrow and tall, with a white area | Set `isLandscape: false` next to `screenshotValidation`. |
| A step is `unresolved` on every run without a visible change | The page was still loading. Wait for fonts and images before tracking, or draw an ignore area over the dynamic region in the comparison view. |
| All runs end up in one entry in **Runs** | The suite name is constant. Add a timestamp or build ID to it. |

Another framework or language? Send screenshots through the [GraphQL API](graphql-api.md).
