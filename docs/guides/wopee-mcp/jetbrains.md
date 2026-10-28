---
title: Add the Wopee.io MCP server to JetBrains AI Assistant and Junie
description: Set up the Wopee.io MCP server in JetBrains IDEs (IntelliJ IDEA, WebStorm, PyCharm and others) for AI Assistant and Junie. Settings path, .junie/mcp/mcp.json, API key, verify and troubleshooting.
type: How-to
updated: 27 October 2026
---

# Add the Wopee.io MCP server to JetBrains AI Assistant and Junie

Connect JetBrains AI Assistant or Junie to your Wopee.io project, so the agent can generate tests, run them with Wopee.io's testing agent and read the verdicts. Works in IntelliJ IDEA, WebStorm, PyCharm and the other JetBrains IDEs. What the server does: [Wopee.io MCP server](index.md).

Before you start: Node.js 20.18 or newer, and `WOPEE_API_KEY` and `WOPEE_PROJECT_UUID` from **More** › **Settings** › **API Keys** in your project ([how](index.md#1-get-your-api-key-and-project-uuid)).

The configuration for both:

```json
{
  "mcpServers": {
    "wopee": {
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

## JetBrains AI Assistant

1. Open **Settings** › **Tools** › **AI Assistant** › **Model Context Protocol (MCP)**.
2. Click **Add** and paste the JSON above, with your values.
3. Choose whether the server is available globally or only in this project, and click **Apply**.

### Verify in AI Assistant

The **Status** column in the same settings page shows whether the server runs. Logs are under **Help** › **Show Log**, in the `mcp` folder.

## Junie

Junie in the IDE and the Junie CLI read the same files.

### Junie MCP config file location

| Scope | File |
| --- | --- |
| Project | `.junie/mcp/mcp.json` |
| User | `~/.junie/mcp/mcp.json` |

Save the JSON above in one of them.

### Verify in Junie

Run `/mcp` in Junie.

## Pass your Wopee.io API key securely

The configuration contains the key. Keep it in the IDE settings or in the user file `~/.junie/mcp/mcp.json`. If you use the project file `.junie/mcp/mcp.json`, add it to `.gitignore` or keep the key out of it.

## First prompt to try

```text
How many tests do I have in Wopee.io, and which ones have never run?
```

The agent calls `wopee_fetch_test_inventory` and lists the analyses and test cases in your project with their latest status. More prompts: [Prompt library](index.md#prompt-library).

## Troubleshooting

| Problem | Fix |
| --- | --- |
| The status shows an error | Open **Help** › **Show Log** and the `mcp` folder. Usually Node.js is older than 20.18, or the IDE does not find `npx`; use its full path in `command` |
| `[AUTH_ERROR] WOPEE_API_KEY or WOPEE_AUTH_TOKEN must be set` | The `env` block is missing or empty |

All error messages and their fixes: [Troubleshooting](index.md#troubleshooting).

## FAQ

### How do I add an MCP server to IntelliJ IDEA?

In AI Assistant: **Settings** › **Tools** › **AI Assistant** › **Model Context Protocol (MCP)** › **Add**. For Junie: add it to `.junie/mcp/mcp.json` or `~/.junie/mcp/mcp.json`.

### Where is the Junie MCP config file?

`.junie/mcp/mcp.json` in the project and `~/.junie/mcp/mcp.json` in your home folder.
