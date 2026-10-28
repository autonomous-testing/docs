---
title: Add the Wopee.io MCP server to Visual Studio
description: Set up the Wopee.io MCP server for GitHub Copilot in Visual Studio 2026 and 2022 (17.14+). Config file locations (.mcp.json, .vs/mcp.json), enable the tools, verify and troubleshooting.
type: How-to
updated: 27 October 2026
---

# Add the Wopee.io MCP server to Visual Studio

Connect GitHub Copilot in Visual Studio 2026 or Visual Studio 2022 (17.14 or newer) to your Wopee.io project, so the agent can generate tests, run them with Wopee.io's testing agent and read the verdicts. What the server does: [Wopee.io MCP server](index.md).

Before you start: Node.js 20.18 or newer, and `WOPEE_API_KEY` and `WOPEE_PROJECT_UUID` from **More** › **Settings** › **API Keys** in your project ([how](index.md#1-get-your-api-key-and-project-uuid)).

## Add the server

In Copilot Chat, switch to **Agent** mode, open **Tools**, click **+** and choose **Add custom MCP server**. Or create the file yourself:

```json title="%USERPROFILE%\.mcp.json"
{
  "servers": {
    "wopee": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "wopee-mcp"],
      "env": {
        "WOPEE_API_KEY": "your-api-key",
        "WOPEE_PROJECT_UUID": "your-project-uuid"
      }
    }
  }
}
```

## Visual Studio MCP config file location

Visual Studio looks for MCP configuration in this order:

1. `%USERPROFILE%\.mcp.json` (you, all solutions)
2. `<solution folder>\.vs\mcp.json`
3. `<solution folder>\.mcp.json`
4. `.vscode\mcp.json`
5. `.cursor\mcp.json`

So a `.vscode/mcp.json` set up for [VS Code](github-copilot.md#add-to-vscodemcpjson) is picked up too.

## Pass your Wopee.io API key securely

Keep the entry with the key in `%USERPROFILE%\.mcp.json`, which is outside your repository. Do not commit a solution-level file that contains the key.

## Verify the Wopee.io MCP server is connected

Open the tools picker in Copilot Chat (Agent mode). The tools of a new server are **disabled by default**: enable the `wopee` tools there.

## First prompt to try

```text
How many tests do I have in Wopee.io, and which ones have never run?
```

Copilot calls `wopee_fetch_test_inventory` and lists the analyses and test cases in your project with their latest status. More prompts: [Prompt library](index.md#prompt-library).

## Troubleshooting

| Problem | Fix |
| --- | --- |
| Copilot does not call the Wopee.io tools | Enable them in the tools picker; they are off by default |
| The server is not found | Check the file location and that the top-level key is `servers` |
| `[AUTH_ERROR] WOPEE_API_KEY or WOPEE_AUTH_TOKEN must be set` | The `env` block is missing or empty |

All error messages and their fixes: [Troubleshooting](index.md#troubleshooting).
