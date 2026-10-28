---
title: Configuration and listener
description: Configure wopee_rf for Robot Framework. All environment variables, the keywords, the listener, SeleniumLibrary, branches, CI, and how to fail a test on a visual difference.
type: Reference
updated: 19 October 2026
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
| `WOPEE_BROWSER`, `WOPEE_OS`, `WOPEE_DEVICE`, `WOPEE_VIEWPORT` | no | | Environment labels stored with every screenshot. |
| `WOPEE_CUSTOM_TAGS`, `WOPEE_COMMENT` | no | | Tags and a comment stored with every screenshot. |
| `WOPEE_PIXEL_TO_PIXEL_DIFF_TOLERANCE` | no | | Pixel difference in percent that still counts as a match, for example `0.1`. |
| `WOPEE_TRACKED_KEYWORDS` | listener only | | Keywords after which the listener takes a screenshot, separated by `;`. |
| `WOPEE_EXECUTION_NAME` | listener only | Robot suite name | Name of the run in Commander. |

A wrong value stops the run with a message that names the variable, for example:

```text
Environment variable: WOPEE_DRIVER_LIBRARY (enum: Input should be 'BrowserLibrary', 'NoLibrary' or 'SeleniumLibrary')
```

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

All arguments are named: `Track Fullpage    step_name=Home`. The optional parameters are `browser`, `os`, `device`, `viewport`, `custom_tags`, `comment` and `pixel_to_pixel_diff_tolerance`; they override the matching environment variable for one step ([example](04-some-more-examples.md#more-parameters-for-tracking)).

The three tracking keywords return the result with `step_name`, `status` (`new`, `ok`, `unresolved` or `autoApproved`) and `image_url`, the link to the step in Commander.

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

```shell
export WOPEE_TRACKED_KEYWORDS="Browser.New Page;Browser.Wait For Elements State"
export WOPEE_EXECUTION_NAME="Robot Framework listener $(date '+%Y-%m-%d %H:%M')"
robot -d reports --listener 'wopee_rf.Listener:dot_env_path=.env' tests/saucedemo_listener.robot
```

On Windows, quote the listener argument with double quotes: `--listener "wopee_rf.Listener:dot_env_path=.env"`.

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

```text
Robot Framework listener: login
step_name='Browser.New Page-1' image_url='https://cmd.wopee.io/tests?...' status='new'
step_name='Browser.Wait For Elements State-2' image_url='https://cmd.wopee.io/tests?...' status='new'
| PASS |
```

- The scenario is named after the test case, and steps after the keyword plus a counter (`Browser.New Page-1`). Adding a tracked keyword in the middle of a test renames the steps after it, and they start again as `new`.
- Without `WOPEE_EXECUTION_NAME` the run is named after the Robot suite, so every run of the same file goes to the same run in Commander. Set a unique execution name per run.
- Pass `.robot` files rather than a folder. For a folder the listener also starts a run for the folder suite and logs `[ ERROR ] SeleniumLibrary is not initialized.` because no browser library is loaded at that level. The message is harmless.

## SeleniumLibrary

Install SeleniumLibrary next to the Browser library package:

```shell
pip install robotframework-seleniumlibrary
```

Keep `robotframework-browser` installed: `wopee_rf` 2.6.3 imports it even when you use SeleniumLibrary or only `Track`, and fails with `ModuleNotFoundError: No module named 'Browser'` without it. `rfbrowser init` is not needed in that case.

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

By default a visual difference does not fail the Robot test: the run stays green and you review the result in Commander. Set `WOPEE_ENABLE_SOFT_ASSERT=false` to fail the test when a step is `unresolved`. `Track Fullpage` then stops the scenario and fails with:

```text
Failed due to an unresolved status during visual validation.
```

In listener mode the tracked keyword and the test are marked as failed.

## Branches

Every run belongs to a branch, `master` unless you set `WOPEE_BRANCH_NAME`. Commander shows the branch on the run (`Branch:`) and, on each step, the branch and the baseline branch it was compared with (`Branch:`, `Baseline branch:`). A run with the same suite name and branch is reused, so the branch name is part of what identifies a run.

In CI, set the branch from your pipeline, for example `WOPEE_BRANCH_NAME=$GITHUB_REF_NAME` in GitHub Actions.

## Run in CI

Set the variables as secrets instead of committing `.env`. The library then reads them from the environment and `dot_env_path` can point to a file that does not exist. GitHub Actions example:

```yaml
- name: Visual tests
  env:
    WOPEE_API_URL: https://api.wopee.io
    WOPEE_PROJECT_UUID: ${{ secrets.WOPEE_PROJECT_UUID }}
    WOPEE_API_KEY: ${{ secrets.WOPEE_API_KEY }}
    WOPEE_SCREENSHOT_VALIDATION_ENABLED: "true"
    WOPEE_DRIVER_LIBRARY: BrowserLibrary
    WOPEE_BRANCH_NAME: ${{ github.ref_name }}
  run: robot -d reports -v "SUITE:CI ${{ github.run_number }}" tests/
```

## Troubleshooting

| Symptom | Cause and fix |
| --- | --- |
| `Importing library 'wopee_rf.Standalone' failed: ModuleNotFoundError: No module named 'wopee_sdk'` | Install `wopee_sdk` from inside the package, see [Getting started › Install](01-getting-started.md#3-install). |
| `ModuleNotFoundError: No module named 'Browser'` | Install `robotframework-browser`, also for SeleniumLibrary and `Track`. |
| Test passes, nothing appears in Commander, `${result}` is `None` | `WOPEE_SCREENSHOT_VALIDATION_ENABLED=true` or `WOPEE_DRIVER_LIBRARY` is missing, or `.env` is not found because `robot` runs from another directory. |
| `Keyword 'wopee_rf.Standalone.Track Fullpage' expected 0 non-named arguments, got 1.` or `missing named-only argument 'step_name'` | Name every argument: `step_name=...`. The old `payload=&{payload}` form is not supported. |
| `WopeeError: There is no Suite started, and no suite_name provided.` | Call `Start Suite` in the same test case before `Start Scenario`, or pass `suite_name=` to `Start Scenario`. |
| Steps of a new run appear in an old run | The suite name was reused. Add a timestamp or build number to it. |
| A step stays `new` on the second run | The step from the first run was not approved. Approve it in **Runs**. |
