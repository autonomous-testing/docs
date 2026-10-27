---
title: Add the Wopee.io MCP server to Google Antigravity and Gemini CLI
description: Set up the Wopee.io MCP server in Google Antigravity (app, IDE, CLI) with mcp_config.json and in Gemini CLI with gemini mcp add or settings.json. Config file locations, API key, verify with /mcp, troubleshooting.
---

# Add the Wopee.io MCP server to Google Antigravity and Gemini CLI

Connect Google Antigravity or Gemini CLI to your Wopee.io project, so the agent can generate tests, run them with Wopee.io's testing agent and read the verdicts. What the server does: [Wopee.io MCP server](index.md).

Before you start: Node.js 20.18 or newer, and `WOPEE_API_KEY` and `WOPEE_PROJECT_UUID` from **More** › **Settings** › **API Keys** in your project ([how](index.md#1-get-your-api-key-and-project-uuid)).

## Google Antigravity

The Antigravity app, IDE and CLI read the same `mcp_config.json`.

### Antigravity MCP config file location

| Scope | File |
| --- | --- |
| Global | `~/.gemini/config/mcp_config.json` |
| Workspace | `.agents/mcp_config.json` in the workspace |

### Add to mcp_config.json

```json title="~/.gemini/config/mcp_config.json"
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

### Pass your Wopee.io API key securely

Put the entry with the key in the global file, which stays in your home folder. If you use the workspace file `.agents/mcp_config.json` with a real key, add it to `.gitignore`.

### Verify in Antigravity

- CLI: `/mcp`
- IDE: the **...** menu › **MCP Servers** › **Manage** › **View raw config**
- App: **Settings** › **Customizations**

## Gemini CLI

### Add with the Gemini CLI

```shell
gemini mcp add -s user -e 'WOPEE_API_KEY=${WOPEE_API_KEY}' -e 'WOPEE_PROJECT_UUID=${WOPEE_PROJECT_UUID}' wopee npx -y wopee-mcp
```

### Gemini CLI MCP config file location

| Scope | File |
| --- | --- |
| User | `~/.gemini/settings.json` |
| Project | `.gemini/settings.json` in the project |

```json title="~/.gemini/settings.json"
{
  "mcpServers": {
    "wopee": {
      "command": "npx",
      "args": ["-y", "wopee-mcp"],
      "env": {
        "WOPEE_API_KEY": "${WOPEE_API_KEY}",
        "WOPEE_PROJECT_UUID": "${WOPEE_PROJECT_UUID}"
      },
      "timeout": 300000
    }
  }
}
```

### Pass your Wopee.io API key securely

Gemini CLI replaces `$VAR` and `${VAR}` in `env` with values from its environment. Export `WOPEE_API_KEY` and `WOPEE_PROJECT_UUID` before you start `gemini`.

### Verify in Gemini CLI

Run `gemini mcp list`, or `/mcp` in a session. In a folder you have not trusted, local servers stay disconnected until you run `gemini trust`.

## First prompt to try

```text
How many tests do I have in Wopee.io, and which ones have never run?
```

The agent calls `wopee_fetch_test_inventory` and lists the analyses and test cases in your project with their latest status. More prompts: [Prompt library](index.md#prompt-library).

## Troubleshooting

| Problem | Fix |
| --- | --- |
| Gemini CLI: the server stays disconnected | Trust the folder with `gemini trust` |
| `[AUTH_ERROR] WOPEE_API_KEY or WOPEE_AUTH_TOKEN must be set` | The key is missing in `env`, or the variable was not exported before start |
| Generation calls time out | Raise `timeout` (milliseconds) in the server entry; generations can take up to 5 minutes |

All error messages and their fixes: [Troubleshooting](index.md#troubleshooting).

## FAQ

### Where is the Antigravity MCP config file?

`~/.gemini/config/mcp_config.json` for all workspaces, and `.agents/mcp_config.json` in a workspace.

### Where is the Gemini CLI MCP config file?

`~/.gemini/settings.json` for the user, and `.gemini/settings.json` in a project.
