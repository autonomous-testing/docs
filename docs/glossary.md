# 📖 Glossary

### Baseline

An initial screenshot or snapshot of a specific view in your website or application that matches your visual expected result. This serves as a reference point for comparison during future test runs following updates or releases. Once a screenshot is approved, it becomes the new baseline for that particular step.

### Project

To utilize wopee.io, you must create a project, providing essential details such as the project name and your website's URL. There are two types of projects:

- **Bot Project**: Uses the provided URL to crawl your application and locate elements for interaction.
- **Integration Project**: Involves a more advanced setup within your existing pipelines. This allows you to attach visual validation to previously written automation tests.

### Branch

Similar to tracking versioning during development, branches can be used to store and track particular baselines, meaning each branch can have its own, unique set of baselines. This feature is primarily used for integration projects.

### Test Run (or Suite)

A reference created with every successful launch of the bot for your projects. Each run contains a set of scenarios, which are the next level of nested data within a run.

### Test Scenario

Each successful test run includes at least one scenario, comprising sequences of steps. You can specify the desired number of scenarios and steps for the bot to create or take either in your project configuration or during the setup of bot execution for a specific run, without overwriting your defaults.

### Test Result

A summary of a run calculated from the statuses of each nested entity within a run (scenarios and steps).

### Test Step

An action performed by the bot, documented with a screenshot or snapshot for reference. This reference can be approved as a baseline and used for regression testing in future runs.

### Test Step Status

Indicates the current state of a particular step:

- **New**: No baseline exists for the step.
- **OK**: A baseline exists, and the difference compared to the new screenshot is within the allowed threshold.
- **Unresolved**: A baseline exists, but the difference compared to the new screenshot exceeds the allowed threshold, indicating a change or potential bug.
- **Failed**: A user has rejected the screenshot/snapshot of the step, indicating it should not be set as the new baseline.
- **Approved**: A user has approved the step, designating it as the baseline for subsequent runs.
- **Auto Approved**: An integration feature where a baseline from any other branch exists, and the difference with the new screenshot is within the allowed threshold. With the 'Auto Approve' feature enabled, the step status is automatically set to 'Auto Approved' in such scenarios.
