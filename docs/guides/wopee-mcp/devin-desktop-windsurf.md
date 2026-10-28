---
title: Add the Wopee.io MCP server to Devin Desktop (formerly Windsurf)
description: Set up the Wopee.io MCP server in Devin Desktop, formerly Windsurf, with mcp_config.json. Config file location, API key with ${env:VAR}, verify in Cascade, Devin cloud setup and troubleshooting.
type: How-to
updated: 27 October 2026
---

# Add the Wopee.io MCP server to Devin Desktop (formerly Windsurf)

Windsurf is now called Devin Desktop. Connect its agent (Cascade) to your Wopee.io project, so it can generate tests, run them with Wopee.io's testing agent and read the verdicts. What the server does: [Wopee.io MCP server](index.md).

Before you start: Node.js 20.18 or newer, and `WOPEE_API_KEY` and `WOPEE_PROJECT_UUID` from **More** › **Settings** › **API Keys** in your project ([how](index.md#1-get-your-api-key-and-project-uuid)).

## Add to mcp_config.json

```json title="~/.config/devin/mcp_config.json"
{
  "mcpServers": {
    "wopee": {
      "command": "npx",
      "args": ["-y", "wopee-mcp"],
      "env": {
        "WOPEE_API_KEY": "${env:WOPEE_API_KEY}",
        "WOPEE_PROJECT_UUID": "${env:WOPEE_PROJECT_UUID}"
      }
    }
  }
}
```

## Devin Desktop MCP config file location

| System | File |
| --- | --- |
| macOS, Linux | `~/.config/devin/mcp_config.json` (or `$XDG_CONFIG_HOME/devin/mcp_config.json`) |
| Windows | `%APPDATA%\devin\mcp_config.json` |
| Older Windsurf builds | `~/.codeium/windsurf/mcp_config.json` |

## Pass your Wopee.io API key securely

`${env:WOPEE_API_KEY}` reads the variable from the environment Devin Desktop was started with. `${file:/path/to/file}` reads the value from a file instead.

## Verify the Wopee.io MCP server is connected

In the Cascade panel, open the **...** menu › **MCPs**. The `wopee` server lists 15 tools. Devin Desktop allows up to 100 tools across all servers; disable tools you do not need if you reach the limit.

## Devin (cloud)

In Devin on the web, go to **Customize** › **MCPs** › **Add MCP** › **Add custom MCP** and choose **STDIO**:

- Command: `npx`
- Arguments: `-y wopee-mcp`
- Environment variables: `WOPEE_API_KEY` and `WOPEE_PROJECT_UUID`, taken from Devin Secrets

Local (stdio) servers can only be checked inside a Devin session.

## First prompt to try

```text
How many tests do I have in Wopee.io, and which ones have never run?
```

Cascade calls `wopee_fetch_test_inventory` and lists the analyses and test cases in your project with their latest status. More prompts: [Prompt library](index.md#prompt-library).

## Troubleshooting

| Problem | Fix |
| --- | --- |
| The server does not appear | Check the file path for your version (Devin Desktop or older Windsurf) and that the JSON is valid, then restart |
| `[AUTH_ERROR] WOPEE_API_KEY or WOPEE_AUTH_TOKEN must be set` | Devin Desktop does not see the variables. Start it from a terminal, or use `${file:...}` |
| Too many tools | Disable unused tools or servers; the limit is 100 tools in total |

All error messages and their fixes: [Troubleshooting](index.md#troubleshooting).

## FAQ

### Does the Wopee.io MCP server work with Windsurf?

Yes. Windsurf is now Devin Desktop; use the configuration on this page. Older Windsurf builds read `~/.codeium/windsurf/mcp_config.json`.

### Where is the Devin Desktop MCP config file?

`~/.config/devin/mcp_config.json` on macOS and Linux, `%APPDATA%\devin\mcp_config.json` on Windows.
