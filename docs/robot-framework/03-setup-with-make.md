---
title: Setup with Make
description: Start Wopee.io visual testing for Robot Framework from the template project. Install with one make command and run the Browser, Selenium, listener and image examples.
type: How-to
updated: 3 November 2026
---

# Setup with make

The [Robot Framework template project](https://github.com/Wopee-io/robotframework-template) contains a ready test, examples for every way of using `wopee_rf` and a Makefile that installs everything. Commander creates a repository from it for every Robot Framework project; clone that repository instead of the public template to start with your project UUID filled in.

`make` needs a bash shell: on Windows use WSL or Git Bash, or follow [Getting started](01-getting-started.md).

## Prerequisites

- Python 3.11 or newer (on macOS `python3` is often 3.9), Node.js 22 or newer, `make` and `git`
- A Wopee.io project with test framework **Robot Framework** and an API key: follow steps 1 and 2 of [Getting started](01-getting-started.md)

## Install

```shell
git clone https://github.com/Wopee-io/robotframework-template
cd robotframework-template
make install
```

`make install` creates `.venv`, installs `requirements.txt` (including `wopee_rf` with its `wopee_sdk` dependency), runs `rfbrowser init` and copies `.env.example` to `.env`. `rfbrowser init` downloads Chromium, Firefox and WebKit, which takes a few minutes.

## Configure

Edit `.env`:

```dotenv
WOPEE_PROJECT_URL=https://www.saucedemo.com
WOPEE_PROJECT_UUID=your-project-uuid
WOPEE_API_KEY=your-api-key
WOPEE_SCREENSHOT_VALIDATION_ENABLED=true
WOPEE_DRIVER_LIBRARY=BrowserLibrary
```

Paste your API key after `WOPEE_API_KEY=` and copy `WOPEE_PROJECT_UUID` from **More › Settings › API Keys** in Commander. Add `WOPEE_API_URL` only for an instance other than cmd.wopee.io. `WOPEE_PROJECT_URL` is the app the template tests open. The make targets set `WOPEE_DRIVER_LIBRARY` themselves; the value in `.env` matters only when you run `robot` directly.

`.env.example` also lists `WOPEE_RUN_NAME` and `WOPEE_CI_BUILD_ID`. Nothing reads them. All supported variables are listed in [Configuration and listener › Configuration](02-manual-setup.md#configuration).

## Run

```shell
make test
```

Runs `tests/simple.robot` with the Browser library: it opens `WOPEE_PROJECT_URL`, starts a suite named `Suite name-<timestamp>` and tracks the landing page. The run appears in Commander under **Runs** with the step `Landing page` in status `new`. Approve it, run `make test` again and the step is `ok`.

## Examples

The `test-examples/` folder holds one example per integration. Run them with the template's virtual environment active (`source .venv/bin/activate`):

| Example | Command |
| --- | --- |
| Browser library, keywords | `WOPEE_DRIVER_LIBRARY=BrowserLibrary robot -d reports test-examples/browser_standalone.robot` |
| SeleniumLibrary, keywords | `WOPEE_DRIVER_LIBRARY=SeleniumLibrary robot -d reports test-examples/selenium_standalone.robot` |
| Browser library, listener | `WOPEE_DRIVER_LIBRARY=BrowserLibrary WOPEE_TRACKED_KEYWORDS="Browser.Click;BuiltIn.Log" robot -d reports --listener 'wopee_rf.Listener:dot_env_path=.env' test-examples/browser_listener.robot` |
| SeleniumLibrary, listener | `WOPEE_DRIVER_LIBRARY=SeleniumLibrary WOPEE_TRACKED_KEYWORDS="SeleniumLibrary.Click Link;SeleniumLibrary.Click Button;BuiltIn.Log" robot -d reports --listener 'wopee_rf.Listener:dot_env_path=.env' test-examples/selenium_listener.robot` |
| Any image (`Track`) | `WOPEE_DRIVER_LIBRARY=NoLibrary robot -d reports test-examples/agnostic_standalone.robot` (captures the image with SeleniumLibrary and Chrome) |
| GraphQL API | `make test.api` |

`make test.api` runs `test-examples/api_integration.robot`, which calls the Wopee.io API directly. See `API_INTEGRATION.md` in the template.

## Clean up

```shell
make clean
```

Removes `reports/` and `screenshots/`. The runs stay in Commander.
