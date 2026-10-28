---
description: Definitions of key Wopee.io concepts including baselines, projects, branches, test runs, scenarios, steps, and comparison modes.
---

# Glossary

### Baseline

The approved screenshot of a step: the expected look of a view in your website or application. Later runs are compared with it. Once you approve a screenshot, it becomes the new baseline for that step.

A baseline is identified by `<scenario name>-<step name>` together with the branch and the optional OS, browser, viewport, device and custom tags labels. Renaming a scenario or a step starts a new baseline. Approved baselines are listed under **More** › **Baselines**.

### Project

To utilize wopee.io, you must create a project, providing essential details such as the project name and your website's URL. There are two types of projects:

- **Bot Project**: Uses the provided URL to crawl your application and locate elements for interaction.
- **Integration Project**: Receives screenshots from your own tests in Playwright, Cypress, WebdriverIO, Robot Framework or any other stack, through the SDKs or the [GraphQL API](graphql-api.md). Created with **Explore the app and generate tests** switched off. See [Visual testing with your own tests](visual-testing.md).

### Branch

Similar to tracking versioning during development, branches can be used to store and track particular baselines, meaning each branch can have its own, unique set of baselines. This feature is primarily used for integration projects. The SDKs use the branch `master` unless you set another one (`WOPEE_BRANCH_NAME` or the `branchName` option). Baselines of one branch can be merged into another under **More** › **Baselines** › **Merge Branches**.

### Test Run (or Suite)

One run of your tests, listed under **Runs**. The bot creates one with every launch; your own tests create one with `startSuite` (or the equivalent keyword or command). Each run contains a set of scenarios, which are the next level of nested data within a run.

For integration projects, a suite with the same name on the same branch is reused, so the next run adds to the existing entry. Put a timestamp or a build number into the suite name to get one entry per run.

### Test Scenario

Each successful test run includes at least one scenario, comprising sequences of steps. In integration projects a scenario is usually one test, started with `startScenario`. Its name is part of the baseline key. For the bot, you can specify the desired number of scenarios and steps for the bot to create or take either in your project configuration or during the setup of bot execution for a specific run, without overwriting your defaults.

### Test Result

A summary of a run calculated from the statuses of each nested entity within a run (scenarios and steps).

### Test Step

An action performed by the bot, documented with a screenshot or snapshot for reference. In integration projects, a step is one tracked screenshot (for example `trackFullPage` or `Track Fullpage`). This reference can be approved as a baseline and used for regression testing in future runs.

### Test Step Status

Indicates the current state of a particular step:

- **New**: No baseline exists for the step.
- **OK**: A baseline exists, and the difference compared to the new screenshot is within the allowed threshold.
- **Unresolved**: A baseline exists, but the difference compared to the new screenshot exceeds the allowed threshold, indicating a change or potential bug.
- **Failed**: A user has rejected the screenshot/snapshot of the step, indicating it should not be set as the new baseline.
- **Approved**: A user has approved the step, designating it as the baseline for subsequent runs.
- **Auto Approved**: An integration feature where a baseline from any other branch exists, and the difference with the new screenshot is within the allowed threshold. With the 'Auto Approve' feature enabled, the step status is automatically set to 'Auto Approved' in such scenarios.

The SDKs return the status of each tracked step as `new`, `ok`, `unresolved` or `autoApproved`. A step that is `unresolved` does not fail your test: you review it in **Runs**.
