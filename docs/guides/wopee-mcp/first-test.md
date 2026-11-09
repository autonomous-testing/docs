---
title: Your first test from your coding agent
description: Run your first Wopee.io test from Claude Code, Cursor, Copilot or Codex through the MCP server. What the agent asks, what each tool returns (inventory, dispatch, polling, PASSED, FAILED, INCOMPLETE), where to see the run in Commander, and the free plan's step limit.
type: Tutorial
updated: 9 November 2026
steps: true
---

# Your first test from your coding agent

From the first question to a verdict, in your coding agent's chat. Each step shows the prompt to type, the tool your agent calls and what the tool returns, so you and your agent can tell a good answer from a problem.

!!! note "Sample outputs"

    The outputs on this page are **abbreviated examples**. Their layout, field names and fixed messages come from `wopee-mcp` 1.33.0; the identifiers, names, counts and times are placeholders. Your agent usually summarizes the output instead of showing it.

## Before you start

- The Wopee.io MCP server is connected: your agent lists the `wopee` server with 15 tools. Not yet? [Let your agent set it up](../../agent-setup/index.md) or follow the [quick start](index.md#quick-start).
- Your project's app URL is reachable from the internet. The tests run on Wopee.io's cloud runners, so `localhost` does not work.

!!! warning "Free plan: 50 steps every 5 hours"

    On the free plan the testing agent has 50 steps every 5 hours, counted across your projects, and a dispatch is refused when fewer than 5 are left. An analysis runs the tests it generates, so it can use most of the budget. Start your first analysis in Commander, where it does not count, and run one test at a time. Details: [Usage limit right after the first analysis](troubleshooting.md#usage-limit-right-after-the-first-analysis).

## 1. Ask what you have

```text
How many tests do I have in Wopee.io, and which ones have never run?
```

The agent calls `wopee_fetch_test_inventory` (in OpenCode `wopee_wopee_fetch_test_inventory`). It only reads data.

**A new project with no analysis yet** returns this text. The connection works; continue with step 2.

```text
No analyses found in this project yet.
```

**A project with tests** returns JSON with one entry per analysis and one per test case. Abbreviated, with one test case:

```json
{
  "totals": {
    "analyses": 1,
    "regularTests": 12,
    "reusableBlocks": 1
  },
  "analyses": [
    {
      "analysisIdentifier": "A001",
      "suiteUuid": "<analysis-suite-uuid>",
      "name": "<analysis name>",
      "suiteRunningStatus": "FINISHED",
      "regularTestCount": 12,
      "reusableBlockCount": 1,
      "statusSummary": {
        "PASSED": 9,
        "FAILED": 1,
        "NOT_RUN": 2
      },
      "executionHistoryError": null,
      "testCases": [
        {
          "id": "US001:TC001",
          "userStoryId": "US001",
          "userStoryName": "<user story name>",
          "userStoryCategory": "<category>",
          "testCaseId": "TC001",
          "name": "<test case name>",
          "kind": "REGULAR",
          "status": "PASSED",
          "executedAt": "2026-11-09T09:12:44.000Z",
          "executedTestCaseUuid": "<executed-test-case-uuid>",
          "verdictGateDisagreed": false
        }
      ]
    }
  ]
}
```

What to read in it:

- `status` is the latest result of each test case: `PASSED`, `FAILED`, `INCOMPLETE`, a run state such as `IN_PROGRESS`, or `NOT_RUN` for a test that never ran. `UNKNOWN` means the run history could not be read; the reason is in `executionHistoryError`.
- `R001` test cases are reusable blocks (`"kind": "REUSABLE"`). Other tests use them; they do not run on their own and have no status.
- `verdictGateDisagreed: true` marks a pass that a [verdict gate](../../concepts/verdict-integrity.md) did not confirm. Read the report before you trust it.

## 2. No tests yet: run the first analysis

An analysis explores your app at the URL set on the project, writes user stories and generates test cases. It takes several minutes.

- **Recommended: start it in Commander.** Sign up with your app's URL (`https://cmd.wopee.io/signup?url=<your-app-url>`) or click **NEW PROJECT** in Commander, see [Getting started](../../ai-agent.md). On the free plan, your first analysis started there does not count toward the step limit.
- **Through your agent:** "Use Wopee.io to analyze my app and generate tests". The agent calls `wopee_dispatch_analysis`. It cannot pass a URL, a login or cookie settings: the analysis uses what is set on the project in Commander. This analysis counts toward your plan.

When the analysis is finished, ask the question from step 1 again.

## 3. Run one test

Pick one test case from the inventory and name it:

```text
Run the Wopee.io test US001:TC001 and tell me if it passes.
```

A good agent repeats the test case and asks before it starts, because the run uses Wopee.io's runners and your plan. It then calls `wopee_dispatch_agent` with the analysis suite UUID, the analysis identifier and one test case. The tool returns within seconds:

```text
DISPATCH SUCCESSFUL — tests are now RUNNING (not yet completed).

Tracking:
- Suite UUID: <agent-suite-uuid>
- Analysis Suite UUID: <analysis-suite-uuid>
- Analysis Identifier: A001

Test cases dispatched:
- US001:TC001 → executionStatus: IN_PROGRESS
  executedTestCaseUuid: <executed-test-case-uuid>
  runName: Analysis - A001 (US001:TC001), agent, by <your e-mail> [#<run id>]

IMPORTANT: These tests are RUNNING asynchronously. Do NOT report them as passed or failed.
Tell the user their tests are running and results will be available shortly (typically 1-3 minutes).
You will receive a follow-up notification in chat when tests complete with full results.
```

- The run has **started**, it has not passed. `executedTestCaseUuid` is the handle of this run.
- The last line is meant for the assistant inside Commander. Your coding agent gets **no** notification; it has to ask for the result (step 4).
- On plans below Premium, one dispatch takes one test case. Each project accepts one dispatch every 10 seconds.

If the dispatch is refused, the output starts with `DISPATCH FAILED — tests were NOT started.` and gives the reason. For `Usage limit reached`, see [the usage limit](troubleshooting.md#usage-limit-right-after-the-first-analysis).

## 4. Wait for the verdict

A test run usually takes a few minutes. The agent calls `wopee_fetch_recent_executions` until the run has a verdict. While it runs:

```text
Recent test executions (1 most recent):

- US001:TC001 [A001] → IN_PROGRESS (2026-11-09T10:02:11.000Z)
  executedTestCaseUuid: <executed-test-case-uuid>

Suite UUID of most recent: <agent-suite-uuid>
Analysis Identifier of most recent: A001
```

The list holds up to 20 runs of the project, newest first; the agent matches its run by `executedTestCaseUuid`. If your agent stops waiting before a verdict (Copilot gives up after about 45 seconds), ask:

```text
Check the result now.
```

## 5. Read the verdict

When the run is done, the line shows the verdict and the start of the testing agent's report (the first 200 characters):

```text
- US001:TC001 [A001] → PASSED (2026-11-09T10:04:37.000Z)
  executedTestCaseUuid: <executed-test-case-uuid>
  Report: <first 200 characters of the agent's report>...
```

```text
- US001:TC001 [A001] → FAILED (2026-11-09T10:04:37.000Z)
  executedTestCaseUuid: <executed-test-case-uuid>
  Report: <first 200 characters of the agent's report>...
```

```text
- US001:TC001 [A001] → INCOMPLETE (2026-11-09T10:04:37.000Z)
  executedTestCaseUuid: <executed-test-case-uuid>
  Report: <first 200 characters of the agent's report>...
```

| Verdict | What it means | Next |
| --- | --- | --- |
| `PASSED` | The testing agent proved the expected result with evidence | Nothing to do. Ask for the full report if you want the steps |
| `FAILED` | The app did not do what the test expects, or the test is out of date | Ask the agent to read the full report (`wopee_fetch_executed_test_cases`), then fix the app or the test. "File the failed run as a GitHub issue" creates an issue with the evidence |
| `INCOMPLETE` | The run could not prove a result, for example because of an infrastructure problem. It says nothing about your app | Read the report for the reason, then run the test again |

More on verdicts: [Verdict Integrity](../../concepts/verdict-integrity.md).

## 6. See the run in Commander

Open [Commander](https://cmd.wopee.io){: target="\_blank"} and your project. Every run is in **Runs**, and **Scenarios** shows each test case with its last verdict. Click the test case to open its **Report** with every step, what was expected, what the agent verified and a screenshot per step.

## Next

- [Prompt library](index.md#prompt-library): explore a new app, build tests from your own spec, file failures as GitHub issues
- [Team setup](index.md#team-setup): commit the config, not the key, and tell the agent when to test
- [Troubleshooting](troubleshooting.md): every error message and its fix
