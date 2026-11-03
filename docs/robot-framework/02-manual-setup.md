---
title: Configuration and listener
description: Configure wopee_rf for Robot Framework. All environment variables, the keywords, the listener, SeleniumLibrary, branches, CI, and how to fail a test on a visual difference.
type: Reference
updated: 3 November 2026
---

# Configuration and listener

This page covers everything [Getting started](01-getting-started.md) leaves out. Follow steps 1 to 4 there first: create the project, generate the API key, install `wopee_rf` and create `.env`.

## Configuration

`wopee_rf` reads environment variables that start with `WOPEE_`. Pass a `.env` file with `dot_env_path=.env` when you import the library or the listener. The path is relative to the directory you run `robot` from. Variables already set in the shell take precedence over `.env`.

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `WOPEE_API_URL` | no | `https://api.wopee.io` | API endpoint. Copy it from **More › Settings › API Keys**. |
| `WOPEE_PROJECT_UUID` | yes | | Project UUID from **API Keys**. |
| `WOPEE_API_KEY` | yes | | API key from **Generate a new key**. |
| `WOPEE_SCREENSHOT_VALIDATION_ENABLED` | yes | `false` | Must be `true`. With `false` all keywords do nothing. |
| `WOPEE_DRIVER_LIBRARY` | yes, for `Track Fullpage`, `Track Viewport` and the listener | `NoLibrary` | `BrowserLibrary` or `SeleniumLibrary` (exact spelling). With `NoLibrary` only `Track` works. |
| `WOPEE_BRANCH_NAME` | no | `master` | Branch the run and its baselines belong to. |
| `WOPEE_ENABLE_SOFT_ASSERT` | no | `true` | `false` fails the test when a step is `unresolved`. |
| `WOPEE_ENABLE_CONSOLE_LOGS` | no | `false` | `true` prints each tracking result to the console. |
| `WOPEE_VIEWPORT` | no | | Viewport label stored with every screenshot, for example `1920x1080`. |
| `WOPEE_CUSTOM_TAGS`, `WOPEE_COMMENT` | no | | Tags and a comment stored with every screenshot. |
| `WOPEE_PIXEL_TO_PIXEL_DIFF_TOLERANCE` | no | | Pixel difference in percent that still counts as a match, for example `0.1`. |
| `WOPEE_TRACKED_KEYWORDS` | listener only | | Keywords after which the listener takes a screenshot, separated by `;`. |
| `WOPEE_EXECUTION_NAME` | listener only | Robot suite name | Name of the run in Commander. |

A wrong value stops the run with a message that names the variable, for example:

```text
Environment variable: WOPEE_DRIVER_LIBRARY (enum: Input should be 'BrowserLibrary', 'NoLibrary' or 'SeleniumLibrary')
```

Robot then also prints `Execution stopped by user.`; the cause is the line above it.

## Keywords

Import the library after your browser library:

```robotframework
*** Settings ***
Library     Browser
Library     wopee_rf.Standalone    dot_env_path=.env
```

| Keyword | Arguments | What it does |
| --- | --- | --- |
| `Start Suite` | `suite_name=` | Starts a run. A run with the same name on the same branch is reused. |
| `Start Scenario` | `scenario_name=`, optional `suite_name=` | Starts a scenario. With `suite_name=` it also starts the suite. |
| `Track Fullpage` | `step_name=`, optional parameters | Takes a full-page screenshot and compares it. |
| `Track Viewport` | `step_name=`, optional parameters | Takes a screenshot of the visible area and compares it. |
| `Track` | `image_base64=`, `step_name=`, optional parameters | Compares an image you pass in (PNG, base64). Works without a browser library. |
| `Stop Scenario` | | Finishes the scenario. Put it in `Test Teardown`. |

All arguments are named: `Track Fullpage    step_name=Home`. The optional parameters `viewport`, `custom_tags`, `comment` and `pixel_to_pixel_diff_tolerance` override the matching environment variable for one step ([example](04-some-more-examples.md#more-parameters-for-tracking)). The tracking keywords also take `suite_name=` and `scenario_name=` and start the suite and scenario if none is running, so one line is enough:

```robotframework
Track Fullpage    step_name=Home    scenario_name=Home page    suite_name=${SUITE}
```

The three tracking keywords return `None` when `WOPEE_SCREENSHOT_VALIDATION_ENABLED` is not `true` (and `Track Fullpage` / `Track Viewport` also with `NoLibrary`). Otherwise they return the result with `step_name`, `status` (`new`, `ok`, `unresolved` or `autoApproved`) and `image_url`, the link to the step in Commander.

The library is created again for every test case. Call `Start Suite` (or `Start Scenario` with `suite_name=`) in every test; with the same suite name all tests end up in the same run:

```robotframework
*** Variables ***
${SUITE}    Checkout ${{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}}

*** Test Cases ***
Cart
    Start Scenario    scenario_name=Cart       suite_name=${SUITE}
    Track Fullpage    step_name=Cart page

Payment
    Start Scenario    scenario_name=Payment    suite_name=${SUITE}
    Track Fullpage    step_name=Payment page
```

## Listener

The listener adds visual testing to existing tests without changing them. It starts one run per Robot suite, one scenario per test case, and takes a full-page screenshot after every keyword in `WOPEE_TRACKED_KEYWORDS`. Write each keyword as `<Library>.<Keyword>`:

=== "macOS, Linux"

    ```shell
    export WOPEE_TRACKED_KEYWORDS="Browser.New Page;Browser.Wait For Elements State"
    export WOPEE_EXECUTION_NAME="Robot Framework listener $(date '+%Y-%m-%d %H:%M')"
    export WOPEE_ENABLE_CONSOLE_LOGS=true
    robot -d reports --listener 'wopee_rf.Listener:dot_env_path=.env' tests/saucedemo_listener.robot
    ```

=== "PowerShell"

    ```powershell
    $env:WOPEE_TRACKED_KEYWORDS = "Browser.New Page;Browser.Wait For Elements State"
    $env:WOPEE_EXECUTION_NAME = "Robot Framework listener $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
    $env:WOPEE_ENABLE_CONSOLE_LOGS = "true"
    robot -d reports --listener "wopee_rf.Listener:dot_env_path=.env" tests/saucedemo_listener.robot
    ```

Write the keywords without spaces around `;`: `"Browser.Click; BuiltIn.Log"` never matches `BuiltIn.Log`.

The test itself contains no Wopee.io keywords:

```robotframework
*** Settings ***
Library     Browser

Test Setup    New Page    https://www.saucedemo.com

*** Test Cases ***
Robot Framework listener: login
    Fill Text    id=user-name    standard_user
    Fill Text    id=password     secret_sauce
    Click        id=login-button
    Wait For Elements State    css=.inventory_list    visible
```

With `WOPEE_ENABLE_CONSOLE_LOGS=true` the console shows each result (without it, the results are in `reports/log.html`):

```text
Robot Framework listener: login
step_name='Browser.New Page-1' image_url='https://cmd.wopee.io/tests?...' status='new'
step_name='Browser.Wait For Elements State-2' image_url='https://cmd.wopee.io/tests?...' status='new'
| PASS |
```

- The scenario is named after the test case, and steps after the keyword plus a counter (`Browser.New Page-1`). Adding a tracked keyword in the middle of a test renames the steps after it, and they start again as `new`.
- Without `WOPEE_EXECUTION_NAME` the run is named after the Robot suite, so every run of the same file goes to the same run in Commander. Set a unique execution name per run.
- Pass `.robot` files rather than a folder. For a folder the listener also starts a run for the folder suite and logs `[ ERROR ] Browser library is not initialized.` (`SeleniumLibrary is not initialized.` with SeleniumLibrary) because no browser library is loaded at that level. The message is harmless.

## SeleniumLibrary

Install SeleniumLibrary. `robotframework-browser`, Node.js and `rfbrowser init` are not needed:

```shell
pip install "wopee_rf>=2.7.2" robotframework robotframework-seleniumlibrary
```

Set `WOPEE_DRIVER_LIBRARY=SeleniumLibrary` and import SeleniumLibrary instead of Browser:

```robotframework
*** Settings ***
Library     SeleniumLibrary
Library     wopee_rf.Standalone    dot_env_path=.env

Test Teardown    Run Keywords    Stop Scenario    AND    Close Browser

*** Test Cases ***
Home page
    Open Browser      https://www.saucedemo.com    chrome
    Start Scenario    scenario_name=Home    suite_name=Selenium demo
    Track Fullpage    step_name=Login page
```

For the listener, track SeleniumLibrary keywords, for example `WOPEE_TRACKED_KEYWORDS="SeleniumLibrary.Open Browser;SeleniumLibrary.Click Button"`.

## Fail the test on a visual difference

By default a visual difference does not fail the Robot test: the run stays green and you review the result in Commander. Set `WOPEE_ENABLE_SOFT_ASSERT=false` to fail the test when a step is `unresolved`. `Track`, `Track Fullpage` and `Track Viewport` then stop the scenario and fail with:

```text
WopeeError: Failed due to an unresolved status during visual validation.
```

In listener mode the tracked keyword and the test are marked as failed.

## Branches

Every run belongs to a branch, `master` unless you set `WOPEE_BRANCH_NAME`. Commander shows the branch on the run (`Branch:`) and, on each step, the branch and the baseline branch it was compared with (`Branch:`, `Baseline branch:`). A run with the same suite name and branch is reused, so the branch name is part of what identifies a run.

In CI, set the branch from your pipeline: `${{ github.head_ref || github.ref_name }}` in GitHub Actions (on pull requests `github.ref_name` is `<number>/merge`), `$CI_COMMIT_REF_NAME` in GitLab CI, `$BRANCH_NAME` in a Jenkins multibranch pipeline.

## Run in CI

Set the variables as secrets instead of committing `.env`. The library then reads them from the environment and `dot_env_path` can point to a file that does not exist. Projects created in Commander already have a workflow in their repository ([Template project](03-setup-with-make.md)). A complete GitHub Actions job:

```yaml
jobs:
  visual-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - uses: actions/setup-node@v4
        with:
          node-version: "22"
      - run: pip install "wopee_rf>=2.7.2" robotframework robotframework-browser
      - run: rfbrowser init chromium
      - name: Visual tests
        env:
          WOPEE_API_URL: https://api.wopee.io
          WOPEE_PROJECT_UUID: ${{ secrets.WOPEE_PROJECT_UUID }}
          WOPEE_API_KEY: ${{ secrets.WOPEE_API_KEY }}
          WOPEE_SCREENSHOT_VALIDATION_ENABLED: "true"
          WOPEE_DRIVER_LIBRARY: BrowserLibrary
          WOPEE_BRANCH_NAME: ${{ github.head_ref || github.ref_name }}
        run: robot -d reports -v "SUITE:CI ${{ github.run_number }}" tests/
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: robot-reports
          path: reports/
```

`-v SUITE:` works because the test names its run with `${SUITE}` ([Getting started › Write the test](01-getting-started.md#5-write-the-test)). With the listener, set `WOPEE_EXECUTION_NAME` instead.

## Troubleshooting

| Symptom | Cause and fix |
| --- | --- |
| `Importing library 'wopee_rf.Standalone' failed: ModuleNotFoundError: No module named 'wopee_sdk'` | `wopee_rf` older than 2.7.2 does not install `wopee_sdk`. Run `pip install --upgrade wopee_rf`. |
| `ModuleNotFoundError: No module named 'Browser'` | Install `robotframework-browser`, needed for `WOPEE_DRIVER_LIBRARY=BrowserLibrary`. With SeleniumLibrary, `wopee_rf` older than 2.7.2 needs it too: run `pip install --upgrade wopee_rf`. |
| Test passes, nothing appears in Commander, `${result}` is `None`; or `'NoneType' object has no attribute 'status'` | `WOPEE_SCREENSHOT_VALIDATION_ENABLED=true` or `WOPEE_DRIVER_LIBRARY` is missing, or `.env` is not found because `robot` runs from another directory. |
| `API key and project UUID are required` | `WOPEE_API_KEY` in `.env` is empty. Paste the key after `WOPEE_API_KEY=`. |
| `Not Authorised!` or `You are not authorized to get this resource.` | The API key belongs to another project or another Wopee.io instance, or `WOPEE_API_URL` points to the wrong instance. Create the key in the Commander you run against. |
| `pip` cannot find `wopee_rf>=2.7.2`, or installs for many minutes | `python` is older than 3.11 (on macOS `python3` is often 3.9). Create the virtual environment with Python 3.11 or newer. |
| `Keyword 'wopee_rf.Standalone.Track Fullpage' expected 0 non-named arguments, got 1.` or `missing named-only argument 'step_name'` | Name every argument: `step_name=...`. The old `payload=&{payload}` form is not supported. |
| `WopeeError: There is no Suite started, and no suite_name provided.` | Call `Start Suite` in the same test case before `Start Scenario`, or pass `suite_name=` to `Start Scenario`. |
| `WopeeError: There is no Scenario started, and no scenario_name provided.` | Call `Start Scenario` before tracking, or pass `scenario_name=` to the tracking keyword. With `WOPEE_ENABLE_SOFT_ASSERT=false` this also follows an `unresolved` step, which stops the scenario. |
| The listener takes no screenshots | A keyword in `WOPEE_TRACKED_KEYWORDS` does not match exactly: write `<Library>.<Keyword>` and no spaces around `;`. |
| Steps of a new run appear in an old run | The suite name was reused. Add a timestamp or build number to it. |
| A step stays `new` on the second run | The step from the first run was not approved. Approve it in **Runs**. |
