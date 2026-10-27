---
title: Add the Wopee.io MCP server to other MCP clients
description: Wopee.io MCP server configuration for Zed, Cline, Kilo Code, Warp, Kiro, Goose, Continue, Augment and Claude Desktop. Config file locations, API key handling and how to verify each.
---

# Add the Wopee.io MCP server to other MCP clients

Any MCP client that can start a local (stdio) server can use the Wopee.io MCP server. This page has the configuration for clients without their own page. What the server does: [Wopee.io MCP server](index.md).

Before you start: Node.js 20.18 or newer, and `WOPEE_API_KEY` and `WOPEE_PROJECT_UUID` from **More** › **Settings** › **API Keys** in your project ([how](index.md#1-get-your-api-key-and-project-uuid)).

Wherever a configuration below contains `your-api-key`, keep that file out of git.

## Zed

Add to Zed's `settings.json`:

```json title="settings.json"
{
  "context_servers": {
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

Verify: **Settings** › **AI** › **MCP Servers**. A green dot means the server is active.

## Cline

In the Cline panel, click the **MCP Servers** icon › **Configure** › **Configure MCP Servers**. This opens `cline_mcp_settings.json`. The Cline CLI uses `~/.cline/data/settings/cline_mcp_settings.json` (or the path in `CLINE_MCP_SETTINGS_PATH`).

```json title="cline_mcp_settings.json"
{
  "mcpServers": {
    "wopee": {
      "command": "npx",
      "args": ["-y", "wopee-mcp"],
      "env": {
        "WOPEE_API_KEY": "your-api-key",
        "WOPEE_PROJECT_UUID": "your-project-uuid"
      },
      "disabled": false
    }
  }
}
```

The CLI also has `cline mcp add`. Leave `autoApprove` empty at first, so Cline asks before it starts runs.

## Kilo Code

Kilo Code uses the same format as OpenCode. Add to `kilo.jsonc` or `.kilo/kilo.jsonc` in the project, or `~/.config/kilo/kilo.jsonc` for all projects:

```json title="kilo.jsonc"
{
  "mcp": {
    "wopee": {
      "type": "local",
      "command": ["npx", "-y", "wopee-mcp"],
      "environment": {
        "WOPEE_API_KEY": "{env:WOPEE_API_KEY}",
        "WOPEE_PROJECT_UUID": "{env:WOPEE_PROJECT_UUID}"
      }
    }
  }
}
```

Verify: **Settings** › **Agent Behaviour** › **MCP Servers**.

## Warp

Open **Settings** › **Agents** › **MCP servers** › **+ Add** and paste:

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

Warp also stores servers in `.warp/.mcp.json` (project) and `~/.warp/.mcp.json`, and detects servers you already set up for Claude Code (`~/.claude.json`) and Codex (`~/.codex/config.toml`). Verify on the MCP servers page: start the server and use **View Logs**. Warp removes the `env` values when you share a server.

## Kiro

Kiro IDE and Kiro CLI (formerly Amazon Q Developer CLI) read `.kiro/settings/mcp.json` in the workspace and `~/.kiro/settings/mcp.json`. The workspace file wins when both define the server.

```json title="~/.kiro/settings/mcp.json"
{
  "mcpServers": {
    "wopee": {
      "command": "npx",
      "args": ["-y", "wopee-mcp"],
      "env": {
        "WOPEE_API_KEY": "${WOPEE_API_KEY}",
        "WOPEE_PROJECT_UUID": "${WOPEE_PROJECT_UUID}"
      },
      "disabled": false
    }
  }
}
```

Kiro replaces `${VAR}` only for environment variables you have approved in Kiro.

## Goose

Add to `~/.config/goose/config.yaml`, or use `goose configure` › **Add Extension**:

```yaml title="~/.config/goose/config.yaml"
extensions:
  wopee:
    name: Wopee.io
    type: stdio
    cmd: npx
    args: [-y, wopee-mcp]
    envs:
      WOPEE_API_KEY: your-api-key
      WOPEE_PROJECT_UUID: your-project-uuid
    enabled: true
    timeout: 300
```

Goose also has an install link: [Add to Goose](goose://extension?cmd=npx&arg=-y&arg=wopee-mcp&id=wopee&name=Wopee.io&description=Wopee.io%20MCP%20server){ .md-button }. The link cannot carry environment variables, so add `WOPEE_API_KEY` and `WOPEE_PROJECT_UUID` to the extension afterwards.

## Continue

Create `.continue/mcpServers/wopee.yaml` in your project. MCP tools work in Continue's agent mode only.

```yaml title=".continue/mcpServers/wopee.yaml"
name: Wopee.io
version: 0.0.1
schema: v1
mcpServers:
  - name: wopee
    command: npx
    args:
      - "-y"
      - "wopee-mcp"
    env:
      WOPEE_API_KEY: ${{ secrets.WOPEE_API_KEY }}
      WOPEE_PROJECT_UUID: ${{ secrets.WOPEE_PROJECT_UUID }}
```

## Augment

In Augment (VS Code, JetBrains or the Auggie CLI), open **Settings** › **MCP** and use **Import from JSON** with the [universal configuration](index.md#universal-configuration), or add the server by name and command (`npx -y wopee-mcp`) and enter the two variables in the environment section.

## Claude Desktop

Claude Desktop reads the [universal configuration](index.md#universal-configuration) (`mcpServers` with `command`, `args` and `env`) from its `claude_desktop_config.json`. Put the real values into `env`, restart Claude Desktop and check that the `wopee` tools appear in a new chat.

## Not supported

Agents that accept only remote (HTTP) MCP servers, such as ChatGPT on the web and Replit Agent, cannot start the Wopee.io MCP server, because it runs locally over stdio.

## First prompt to try

```text
How many tests do I have in Wopee.io, and which ones have never run?
```

The agent calls `wopee_fetch_test_inventory` and lists the analyses and test cases in your project with their latest status. More prompts: [Prompt library](index.md#prompt-library). Error messages and fixes: [Troubleshooting](index.md#troubleshooting).
