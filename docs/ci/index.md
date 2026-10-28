---
title: Run Wopee.io in CI
description: Run Playwright, Cypress, WebdriverIO and Robot Framework tests with Wopee.io in any CI system. Secrets, branches, suite names and the MCP server in pipelines.
---

# Run in CI

Wopee.io works with any CI system. Your tests run as they always do; the Wopee.io library or plugin reads its settings from environment variables.

## Secrets

Set these as secrets of your CI instead of committing a `.env` file:

| Variable | Description |
| --- | --- |
| `WOPEE_API_KEY` | Project API key (**More** › **Settings** › **API Keys**). |
| `WOPEE_PROJECT_UUID` | Project UUID (same place). |
| `WOPEE_API_URL` | Only for a self-hosted instance. Default `https://api.wopee.io`. |

## Branches and suite names

- Baselines are kept per branch. Set `WOPEE_BRANCH_NAME` from your pipeline, for example `WOPEE_BRANCH_NAME=$GITHUB_REF_NAME` in GitHub Actions.
- A suite is identified by its name and branch: the same suite name on the same branch adds to the existing entry in **Runs**. Put a timestamp or the CI build number into the suite name.
- See [Baselines and branches](../visual-testing.md#baselines-and-branches) for merging and managing baselines.

## By framework

- **Playwright**: [Configuration](../playwright-visual-testing.md#configuration), all options are environment variables.
- **Cypress**: [Run in CI](../cypress/03-install-plugin.md#run-in-ci) and [Branches and suites](../cypress/03-install-plugin.md#branches-and-suites).
- **WebdriverIO**: [Branches in CI](../webdriverio-visual-testing.md#branches-in-ci).
- **Robot Framework**: [Run in CI](../robot-framework/02-manual-setup.md#run-in-ci) with a GitHub Actions example.
- **Any other stack**: the [GraphQL API](../graphql-api.md) takes the same project key.

## MCP and headless agents

Store `WOPEE_API_KEY` and `WOPEE_PROJECT_UUID` as CI secrets and pin the `wopee-mcp` package version. For scheduled regression runs without an agent, use [Test Plans](../ai-agent.md#7-test-plans-and-schedules) in Commander; they cannot be started through MCP. See the [MCP guide](../guides/wopee-mcp/index.md).
