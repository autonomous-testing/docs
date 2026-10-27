---
title: Add the Wopee.io MCP server to OpenAI Codex
description: Set up the Wopee.io MCP server in OpenAI Codex (CLI, IDE extension and ChatGPT desktop app) with codex mcp add or config.toml. Forward the API key with env_vars, verify with /mcp, first prompt and troubleshooting.
---

# Add the Wopee.io MCP server to OpenAI Codex

Connect OpenAI Codex to your Wopee.io project, so it can generate tests, run them with Wopee.io's testing agent and read the verdicts. The Codex CLI, the Codex IDE extension and the ChatGPT desktop app share one configuration, so you set it up once. What the server does: [Wopee.io MCP server](index.md).

Before you start: Node.js 20.18 or newer, and `WOPEE_API_KEY` and `WOPEE_PROJECT_UUID` from **More** › **Settings** › **API Keys** in your project ([how](index.md#1-get-your-api-key-and-project-uuid)).

## Add to config.toml

Add the server to `~/.codex/config.toml`:

```toml title="~/.codex/config.toml"
[mcp_servers.wopee]
command = "npx"
args = ["-y", "wopee-mcp"]
env_vars = ["WOPEE_API_KEY", "WOPEE_PROJECT_UUID"]
```

`env_vars` passes the two variables from the environment Codex runs in to the server, so the key is not stored in the file.

## Add with the Codex CLI

```shell
codex mcp add wopee --env WOPEE_API_KEY=your-api-key --env WOPEE_PROJECT_UUID=your-project-uuid -- npx -y wopee-mcp
```

This stores the values in `~/.codex/config.toml` in plain text, under `[mcp_servers.wopee.env]`. To keep the key out of the file, use the `env_vars` form above instead.

## Codex MCP config file location

| Scope | File |
| --- | --- |
| User | `~/.codex/config.toml` |
| Project | `.codex/config.toml` in the project, used for trusted projects only |

## Pass your Wopee.io API key securely

Export the variables before you start Codex and use `env_vars`:

```shell
export WOPEE_API_KEY="your-api-key"
export WOPEE_PROJECT_UUID="your-project-uuid"
codex
```

The IDE extension and the desktop app need the variables in the environment they were started from.

## Verify the Wopee.io MCP server is connected

- CLI: `codex mcp list`, or `/mcp` inside a session.
- ChatGPT desktop app: `/mcp` in the composer.
- IDE extension: the gear menu › MCP servers.

## First prompt to try

```text
How many tests do I have in Wopee.io, and which ones have never run?
```

Codex calls `wopee_fetch_test_inventory` and lists the analyses and test cases in your project with their latest status. More prompts: [Prompt library](index.md#prompt-library).

## Troubleshooting

| Problem | Fix |
| --- | --- |
| `[AUTH_ERROR] WOPEE_API_KEY or WOPEE_AUTH_TOKEN must be set` | With `env_vars`, the variables were not set when Codex started. Export them and restart |
| The project `.codex/config.toml` is ignored | Codex reads project config only in trusted projects |
| The server does not start | Run `npx -y wopee-mcp` in a terminal to see the error. Usually Node.js is older than 20.18 |

All error messages and their fixes: [Troubleshooting](index.md#troubleshooting).

## FAQ

### How do I add an MCP server to Codex?

Run `codex mcp add <name> -- <command>`, or add a `[mcp_servers.<name>]` table to `~/.codex/config.toml`.

### Where is the Codex MCP config file?

`~/.codex/config.toml`, or `.codex/config.toml` in a trusted project.

### Does the Wopee.io MCP server work in ChatGPT?

In the ChatGPT desktop app, yes: it uses the Codex configuration. ChatGPT on the web cannot start local MCP servers, and the Wopee.io MCP server has no remote endpoint.
