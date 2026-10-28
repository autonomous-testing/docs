---
title: Setup with Make
description: Start Wopee.io visual testing for Robot Framework from the template project. Install with one make command and run the Browser, Selenium, listener and image examples.
type: How-to
updated: 19 October 2026
---

# Setup with make

The [Robot Framework template project](https://github.com/Wopee-io/robotframework-template) contains a ready test, examples for every way of using `wopee_rf` and a Makefile that installs everything.

## Prerequisites

- Python 3.11 or newer, Node.js 18 or newer, `make` and `git`
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
WOPEE_API_URL=https://api.wopee.io
WOPEE_PROJECT_UUID=your-project-uuid
WOPEE_API_KEY=your-api-key
WOPEE_SCREENSHOT_VALIDATION_ENABLED=true
```

`WOPEE_API_KEY` is commented out in `.env.example`: remove the `#`. Copy `WOPEE_API_URL` and `WOPEE_PROJECT_UUID` from **More › Settings › API Keys** in Commander. The Makefile sets `WOPEE_DRIVER_LIBRARY` for each target, so leave it out of `.env` and make sure it is not exported in your shell (`unset WOPEE_DRIVER_LIBRARY`): a shell variable takes precedence over `.env`.

`.env.example` also lists `WOPEE_PROJECT_URL`, `WOPEE_RUN_NAME` and `WOPEE_CI_BUILD_ID`. `wopee_rf` does not read them. All supported variables are listed in [Configuration and listener › Configuration](02-manual-setup.md#configuration).

## Run

```shell
make test
```

Runs `tests/simple.robot` with the Browser library: it opens the demo app, starts a suite named `Suite name-<timestamp>` and tracks the landing page. The run appears in Commander under **Runs** with the step `Landing page` in status `new`. Approve it, run `make test` again and the step is `ok`.

## Examples

The `test-examples/` folder holds one example per integration. Run them with the template's virtual environment active (`source .venv/bin/activate`):

| Example | Command |
| --- | --- |
| Browser library, keywords | `WOPEE_DRIVER_LIBRARY=BrowserLibrary robot -d reports test-examples/browser_standalone.robot` |
| SeleniumLibrary, keywords | `WOPEE_DRIVER_LIBRARY=SeleniumLibrary robot -d reports test-examples/selenium_standalone.robot` |
| Browser library, listener | `WOPEE_DRIVER_LIBRARY=BrowserLibrary WOPEE_TRACKED_KEYWORDS="Browser.Click;BuiltIn.Log" robot -d reports --listener 'wopee_rf.Listener:dot_env_path=.env' test-examples/browser_listener.robot` |
| SeleniumLibrary, listener | `WOPEE_DRIVER_LIBRARY=SeleniumLibrary WOPEE_TRACKED_KEYWORDS="SeleniumLibrary.Click Link;SeleniumLibrary.Click Button;BuiltIn.Log" robot -d reports --listener 'wopee_rf.Listener:dot_env_path=.env' test-examples/selenium_listener.robot` |
| Any image (`Track`) | `robot -d reports test-examples/agnostic_standalone.robot` |
| GraphQL API | `make test.api` |

`make test.api` runs `test-examples/api_integration.robot`, which calls the Wopee.io API directly. See `API_INTEGRATION.md` in the template.

## Clean up

```shell
make clean
```

Removes `reports/` and `screenshots/`. The runs stay in Commander.
