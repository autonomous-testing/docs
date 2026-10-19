---
title: "Any other framework: the GraphQL API"
description: Send screenshots to Wopee.io from Selenium, TestCafe, Appium, Puppeteer or any custom harness. Endpoint, API key headers, the suite, scenario and step mutations with all fields, a curl walk-through and a Python example.
---

# Any other framework: the GraphQL API

The Playwright, Cypress, WebdriverIO and Robot Framework SDKs are thin clients of one GraphQL API. When your tests run in anything else, such as Selenium (Java, C#, Python), TestCafe, Appium, Puppeteer or your own harness, call the same API directly: take a screenshot the way your tool does it and send it as base64.

This page is the reference for those calls.

Read [Visual testing with your own tests](visual-testing.md) first for the concepts (projects, baselines, branches, review in **Runs**). This page covers only what is different when you call the API yourself.

## Endpoint and authentication

| What | Value |
| --- | --- |
| Endpoint | `https://api.wopee.io/graphql` for [cmd.wopee.io](https://cmd.wopee.io){: target="\_blank"}. Self-hosted: your instance's API URL, shown as `WOPEE_API_URL` in **API Keys**. The API answers on both the root URL and `/graphql`. |
| Method | `POST`, `Content-Type: application/json`, body `{"query": "...", "variables": {...}}` |
| API key | Header `x-api-key: <WOPEE_API_KEY>` |
| Project | `projectUuid` argument of each mutation (`WOPEE_PROJECT_UUID`) |

Get the key and the project UUID in Commander under **More** › **Settings** › **API Keys**, see [Get the API key](visual-testing.md#2-get-the-api-key). The key belongs to one project and works only with that project's UUID.

!!! tip "Use `x-api-key`"

    The API reads the key from the `api_key` header or from `x-api-key`. Some corporate proxies and load balancers drop header names that contain an underscore, so the request arrives without a key. Send `x-api-key`, or both headers with the same value as the SDKs do.

Errors come back in the GraphQL `errors` array. A wrong key returns HTTP `401` with `You are not authorized to get this resource.`; most other errors, a missing key included, return HTTP `200` with `errors` set and the mutation's `data` field `null`. Always check `errors`, not only the HTTP status.

## Lifecycle

```text
createIntegrationSuite      one run of your tests (an entry in Runs)
└─ createIntegrationScenario    one test
   ├─ createIntegrationStep     one screenshot, compared with its baseline
   ├─ createIntegrationStep     ...
   └─ stopIntegrationScenario   the test is finished
stopIntegrationSuite        the run is finished
```

1. **Suite.** `createIntegrationSuite` returns the suite `uuid`. If a suite with the same name already exists on the same branch, you get that suite back and the run adds to it. Put a timestamp or a CI build number into the name to get one entry per run.
2. **Scenario.** `createIntegrationScenario` returns the scenario `uuid`. The same scenario name in the same suite returns the existing scenario.
3. **Steps.** Call `createIntegrationStep` once per screenshot. The response carries the comparison `status` right away.
4. **Stop the scenario** with `stopIntegrationScenario` when the test ends. It sets the scenario to `FINISHED` and the suite to `IDLE`.
5. **Stop the suite** with `stopIntegrationSuite` when the whole run ends. It stops any scenario still in progress and sets the suite to `FINISHED`. The SDKs do not call it; the run is shown in **Runs** either way.

### Naming rules

- The **baseline** of a step is identified by `trackName` + the suite's **branch** + the labels `os`, `browser`, `viewport`, `device` and `customTags`. Change any of them and the step starts a new baseline with status `new`.
- The SDKs send `trackName` as `<scenario name>-<step name>`. Do the same and keep the names stable between runs, so the same check always meets the same baseline.
- The **branch** is `suiteIntegrationConfig.branchName` of the suite. The SDKs default to `master`.
- Within a scenario, a step is matched by `stepName`. Sending the same `stepName` again in the same scenario replaces that step's screenshot instead of adding a new row.
- Do not end step names with `[TS<number>]`, for example `Login [TS001]`. That suffix is reserved for steps of the Wopee.io agent.

### What the status means

`createIntegrationStep` returns `status`:

| Status | Meaning |
| --- | --- |
| `new` | No baseline yet. Approve the screenshot in Commander to make it the baseline. |
| `ok` | Matches the baseline within the tolerance. |
| `unresolved` | Differs from the baseline. Approve it as the new baseline or reject it as a bug. |
| `autoApproved` | Approved automatically by Wopee.io. |
| `approved`, `failed` | The step was already reviewed: approved, or rejected. |

!!! note "A visual difference never fails your test"

    The API only records the result. Your test passes or fails on its own assertions. Review the steps in Commander › **Runs**: **Approve** makes the screenshot the baseline, **Reject** marks it as a bug and the step shows as **Failed**. To fail the test on a difference as well, check the returned `status` yourself, for example fail on anything other than `ok`, `new` and `autoApproved`.

## Mutations

### createIntegrationSuite

Starts a run, or returns the existing suite with the same name on the same branch.

| Argument | Type | Required | Meaning |
| --- | --- | --- | --- |
| `projectUuid` | `ID!` | yes | `WOPEE_PROJECT_UUID` |
| `name` | `String!` | yes | Suite name shown in **Runs** |
| `suiteIntegrationConfig` | `SuiteConfigInput` | yes, in practice | `{ branchName: String }`. The schema marks it optional, but the call fails without it. Send `{ "branchName": "master" }` or your branch. |
| `suiteUuid` | `ID` | no | Attach to this existing suite instead of looking it up by name and branch |

Response `CreateSuiteResponse`: `uuid`, `name`, `projectUuid`, `suiteRunningStatus` (`IN_PROGRESS`, `IDLE`, `FINISHED`, …), `suiteIntegrationConfig { branchName }`.

### createIntegrationScenario

| Argument | Type | Required | Meaning |
| --- | --- | --- | --- |
| `projectUuid` | `ID!` | yes | `WOPEE_PROJECT_UUID` |
| `suiteUuid` | `ID!` | yes | From `createIntegrationSuite` |
| `name` | `String` | recommended | Scenario name, usually the test name. Part of `trackName` by convention. |

Response `CreateScenarioResponse`: `uuid`, `name`, `scenarioRunningStatus` (`IN_PROGRESS`, `FINISHED`).

### createIntegrationStep

Takes one argument, `input: CreateIntegrationStepInput!`:

| Field | Type | Required | Meaning |
| --- | --- | --- | --- |
| `projectUuid` | `ID!` | yes | `WOPEE_PROJECT_UUID` |
| `scenarioUuid` | `ID!` | yes | From `createIntegrationScenario` |
| `stepName` | `String!` | yes | Step name shown in Commander |
| `trackName` | `String!` | yes | Baseline name, by convention `<scenario name>-<step name>` |
| `imageBase64` | `String!` | yes | The screenshot as base64-encoded PNG, without a `data:image/png;base64,` prefix |
| `os` | `String` | no | Label, part of the baseline identity |
| `browser` | `String` | no | Label, part of the baseline identity |
| `viewport` | `String` | no | Label, part of the baseline identity, for example `1280x720` |
| `device` | `String` | no | Label, part of the baseline identity |
| `customTags` | `String` | no | Label, part of the baseline identity |
| `pixelToPixelDiffTolerance` | `Float` | no | Share of differing pixels, in percent, that still counts as `ok`. Default `0`. See [Tolerance](#tolerance-and-environments). |
| `ignoreAreas` | `[{ x: Int!, y: Int!, width: Int!, height: Int! }]` | no | Rectangles in pixels that are left out of the comparison |
| `comment` | `String` | no | Free text stored with the step |
| `baselineBranchName` | `String` | no | Compare with the baseline of this branch, for example `master` while the suite runs on a feature branch. If that branch has no baseline for the step, the current branch's baseline is used. |
| `pageContentBase64` | `String` | no | The page HTML as base64, stored with the step |
| `idempotencyKey` | `String` | no | Your own stable token for this step, so a retry is recognised even if the payload differs. See [Duplicate steps](#duplicate-steps-and-retries). |

Response `CreateIntegrationStepResponse`:

| Field | Meaning |
| --- | --- |
| `status` | `new`, `ok`, `unresolved`, `autoApproved`, `approved` or `failed`, see [the table above](#what-the-status-means) |
| `url` | Link to the step in Commander › **Runs** |
| `diffPercent` | Measured difference in percent (`null` when there is no baseline) |
| `pixelToPixelDiffTolerance` | Tolerance used, in percent |
| `pixelMisMatchCount` | Number of differing pixels |
| `imageName`, `baselineName`, `diffName` | URLs of the screenshot, the baseline and the difference image |
| `branchName`, `baselineBranchName` | Branch of the run and branch of the baseline it was compared with |
| `stepName`, `trackName` | As sent |
| `os`, `browser`, `viewport`, `device`, `customTags`, `comment` | As sent |
| `ignoreAreas`, `tempIgnoreAreas` | Ignore areas as a JSON string |
| `id`, `suiteId`, `testVariationId` | Internal IDs of the comparison |
| `merge`, `createdAt`, `updatedAt` | Internal |

### stopIntegrationScenario

| Argument | Type | Required | Meaning |
| --- | --- | --- | --- |
| `scenarioUuid` | `ID!` | yes | From `createIntegrationScenario` |
| `projectUuid` | `ID!` | yes | `WOPEE_PROJECT_UUID` |

Response `CreateScenarioResponse`: `uuid`, `name`, `scenarioRunningStatus` (`FINISHED`).

### stopIntegrationSuite

| Argument | Type | Required | Meaning |
| --- | --- | --- | --- |
| `suiteUuid` | `ID!` | yes | From `createIntegrationSuite` |
| `forceStop` | `Boolean` | no | Not needed for your own tests |

Response `StopSuiteResponse`: `uuid`, `name`, `suiteRunningStatus` (`FINISHED`).

## Walk-through with curl

The script below runs the whole lifecycle with `curl` and [`jq`](https://jqlang.org){: target="\_blank"}: it starts a suite, starts the scenario **Login**, sends `screenshot.png` as the step **Login page**, and stops the scenario and the suite. `jq` builds the JSON bodies, so the screenshot never has to fit on a command line.

```shell title="Variables"
export WOPEE_API_URL=https://api.wopee.io/graphql
export WOPEE_PROJECT_UUID=your-project-uuid
export WOPEE_API_KEY=your-api-key
```

```bash title="walkthrough.sh"
#!/usr/bin/env bash
set -euo pipefail
SUITE_NAME="My run $(date +%Y-%m-%d_%H%M)"

# Sends one GraphQL request (JSON body on stdin) and prints the JSON response.
gql() {
  curl -sS "$WOPEE_API_URL" \
    -H "Content-Type: application/json" \
    -H "x-api-key: $WOPEE_API_KEY" \
    --data-binary @-
}

# 1. Start (or reuse) a suite on the branch master
jq -n --arg project "$WOPEE_PROJECT_UUID" --arg name "$SUITE_NAME" '{
  query: "mutation ($projectUuid: ID!, $name: String!, $config: SuiteConfigInput) { createIntegrationSuite(projectUuid: $projectUuid, name: $name, suiteIntegrationConfig: $config) { uuid name suiteRunningStatus } }",
  variables: { projectUuid: $project, name: $name, config: { branchName: "master" } }
}' | gql | tee suite.json
SUITE_UUID=$(jq -er '.data.createIntegrationSuite.uuid' suite.json)

# 2. Start a scenario in the suite
jq -n --arg project "$WOPEE_PROJECT_UUID" --arg suite "$SUITE_UUID" '{
  query: "mutation ($projectUuid: ID!, $suiteUuid: ID!, $name: String) { createIntegrationScenario(projectUuid: $projectUuid, suiteUuid: $suiteUuid, name: $name) { uuid name scenarioRunningStatus } }",
  variables: { projectUuid: $project, suiteUuid: $suite, name: "Login" }
}' | gql | tee scenario.json
SCENARIO_UUID=$(jq -er '.data.createIntegrationScenario.uuid' scenario.json)

# 3. Send a screenshot as a step
base64 < screenshot.png | tr -d '\n' > screenshot.b64
jq -n --arg project "$WOPEE_PROJECT_UUID" --arg scenario "$SCENARIO_UUID" --rawfile image screenshot.b64 '{
  query: "mutation ($input: CreateIntegrationStepInput!) { createIntegrationStep(input: $input) { status diffPercent pixelToPixelDiffTolerance branchName baselineBranchName url } }",
  variables: { input: {
    projectUuid: $project,
    scenarioUuid: $scenario,
    stepName: "Login page",
    trackName: "Login-Login page",
    imageBase64: $image,
    browser: "chromium",
    viewport: "1280x720"
  } }
}' | gql | tee step.json
jq -e '.data.createIntegrationStep.status' step.json

# 4. Stop the scenario, then the suite
jq -n --arg project "$WOPEE_PROJECT_UUID" --arg scenario "$SCENARIO_UUID" '{
  query: "mutation ($scenarioUuid: ID!, $projectUuid: ID!) { stopIntegrationScenario(scenarioUuid: $scenarioUuid, projectUuid: $projectUuid) { uuid scenarioRunningStatus } }",
  variables: { scenarioUuid: $scenario, projectUuid: $project }
}' | gql

jq -n --arg suite "$SUITE_UUID" '{
  query: "mutation ($suiteUuid: ID!) { stopIntegrationSuite(suiteUuid: $suiteUuid) { uuid suiteRunningStatus } }",
  variables: { suiteUuid: $suite }
}' | gql
```

Output of a first run (IDs shortened):

```json
{"data":{"createIntegrationSuite":{"uuid":"f39f00d5-…","name":"My run 2026-10-19_1124","suiteRunningStatus":"IN_PROGRESS"}}}
{"data":{"createIntegrationScenario":{"uuid":"b0ed8d3c-…","name":"Login","scenarioRunningStatus":"IN_PROGRESS"}}}
{"data":{"createIntegrationStep":{"status":"new","diffPercent":null,"pixelToPixelDiffTolerance":0,"branchName":"master","baselineBranchName":"master","url":"https://cmd.wopee.io/tests?projectId=…&suiteId=…&stepId=…&tab=RUNS"}}}
"new"
{"data":{"stopIntegrationScenario":{"uuid":"b0ed8d3c-…","scenarioRunningStatus":"FINISHED"}}}
{"data":{"stopIntegrationSuite":{"uuid":"f39f00d5-…","suiteRunningStatus":"FINISHED"}}}
```

Open the `url`, approve the step, and run the script again: the step now returns `ok`, or `unresolved` when the screenshot changed.

## Example in Python

The same flow in Python with [`requests`](https://pypi.org/project/requests/){: target="\_blank"}. It reads a screenshot file that your tool saved, for example with Selenium's `driver.save_screenshot("screenshot.png")`.

```python title="wopee_track.py"
import base64, os, sys
import requests

API_URL = os.environ.get("WOPEE_API_URL", "https://api.wopee.io/graphql")
PROJECT = os.environ["WOPEE_PROJECT_UUID"]
HEADERS = {"x-api-key": os.environ["WOPEE_API_KEY"]}


def gql(query, **variables):
    response = requests.post(API_URL, json={"query": query, "variables": variables}, headers=HEADERS, timeout=180)
    body = response.json()
    if body.get("errors"):
        raise RuntimeError(body["errors"])
    return next(iter(body["data"].values()))


suite = gql("""mutation ($p: ID!, $name: String!, $config: SuiteConfigInput) {
  createIntegrationSuite(projectUuid: $p, name: $name, suiteIntegrationConfig: $config) { uuid } }""",
    p=PROJECT, name=sys.argv[2], config={"branchName": "master"})
scenario = gql("""mutation ($p: ID!, $s: ID!, $name: String) {
  createIntegrationScenario(projectUuid: $p, suiteUuid: $s, name: $name) { uuid name } }""",
    p=PROJECT, s=suite["uuid"], name="Login")

with open(sys.argv[1], "rb") as f:
    image = base64.b64encode(f.read()).decode()
step = gql("""mutation ($input: CreateIntegrationStepInput!) {
  createIntegrationStep(input: $input) { status diffPercent url } }""",
    input={"projectUuid": PROJECT, "scenarioUuid": scenario["uuid"], "stepName": "Login page",
           "trackName": f"{scenario['name']}-Login page", "imageBase64": image, "viewport": "1280x720"})
print(step["status"], step["url"])

gql("mutation ($s: ID!, $p: ID!) { stopIntegrationScenario(scenarioUuid: $s, projectUuid: $p) { uuid } }",
    s=scenario["uuid"], p=PROJECT)
gql("mutation ($s: ID!) { stopIntegrationSuite(suiteUuid: $s) { uuid } }", s=suite["uuid"])
```

```shell
pip install requests
python wopee_track.py screenshot.png "My run 42"
# new https://cmd.wopee.io/tests?projectId=…&suiteId=…&stepId=…&tab=RUNS
```

In a real test suite, create the suite once before all tests, a scenario per test, a step per screenshot, and stop the suite after all tests.

## Duplicate steps and retries

`createIntegrationStep` is safe to retry. When the API receives the same step payload again **within 10 minutes**, it does not create a second screenshot: it returns the answer of the first call. The payload is compared as a whole, so a call that differs in any field, `comment` or `ignoreAreas` included, is new work. Only successful answers are remembered; a retry after an error is processed normally.

- Retry a failed or timed-out call with the identical body. The SDKs use a 180-second timeout per attempt and up to three attempts.
- If your retry cannot be byte-identical, send the same `idempotencyKey` (any stable string per step, for example `<build id>-<scenario>-<step>`) with both attempts. With a key, only the key, the project and the scenario decide whether it is the same call.
- After 10 minutes, an identical call is treated as new: it replaces the step's screenshot in the scenario.

## Tolerance and environments

`pixelToPixelDiffTolerance` is a percentage of differing pixels. With the default `0`, one changed pixel makes the step `unresolved`; with `1.5`, up to 1.5 % of the pixels may differ and the step is still `ok`.

Compare screenshots from the same environment. The same page renders fonts and anti-aliasing differently on macOS, Linux and Windows, and in different browser versions, so a baseline approved on a developer's Mac shows differences against a Linux CI runner. Take the baselines where the tests run in CI, or set `os` (and `browser`) so that each environment gets its own baseline.

## Schema

Introspection is enabled, so you can download the full schema without a key and generate a typed client from it:

```shell
npx get-graphql-schema https://api.wopee.io/graphql > wopee.graphql
```

The schema contains the whole Wopee.io API. Only the mutations on this page are meant for your own tests; the others serve Commander and the Wopee.io agent and can change without notice.
