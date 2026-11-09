---
title: Set up Wopee.io with your coding agent
description: Paste one line into Claude Code, Cursor, GitHub Copilot or Codex and the agent connects the Wopee.io MCP server to your project. What the agent does and changes, prerequisites, manual setup per client and how your API key stays out of the chat.
type: How-to
updated: 9 November 2026
---

# Set up Wopee.io with your coding agent

Paste one line into your coding agent. The agent connects the [Wopee.io MCP server](../guides/wopee-mcp/index.md) to your Wopee.io project, checks the connection with a read-only call and offers to run one test. It shows its plan first and asks before it changes anything.

!!! tip wo-agent-setup "Paste this into your coding agent"

    ```text
    Set me up for Wopee.io: follow https://wopee.io/agent-setup/prompt.md, show me the plan first, and ask before changing anything.
    ```

    The instructions are plain Markdown on our own domain. Read them before you paste: [wopee.io/agent-setup/prompt.md](https://wopee.io/agent-setup/prompt.md){: target="\_blank"}.

The instructions cover Claude Code, Cursor, GitHub Copilot in VS Code and OpenAI Codex, plus a universal configuration for other MCP clients.

## Before you start

- **Node.js 20.18 or newer.** The server runs with `npx`. The agent checks the version and never installs Node.js for you.
- **A Wopee.io project with your app's URL.** No account yet? Sign up with your app's URL, and Commander creates the project and starts the first analysis for you:

    ```text
    https://cmd.wopee.io/signup?url=<your-app-url>
    ```

    The app must be reachable from the internet, because the tests run on Wopee.io's cloud runners. `localhost` does not work.

- **Project admin rights.** Only project admins see **API Keys**, where you get the key and the project UUID. See [Find your API key and project UUID](../guides/api-keys.md).
- **An agent that runs local (stdio) MCP servers.** Web-only chat apps cannot use the server.

## What the agent does

1. **Checks for an existing setup.** If the `wopee` tools already work, it skips to the check in step 6. Running the line again is safe.
2. **Detects your setup and shows a plan.** It works out the client, the operating system and the repository, then lists the files it will change and waits for your yes.
3. **Checks the prerequisites.** `node --version`, `npx --version` and whether the npm registry is reachable. These commands only read.
4. **Adds one MCP server entry named `wopee`.** It runs `npx -y wopee-mcp` and reads `WOPEE_API_KEY` and `WOPEE_PROJECT_UUID` through references such as `${WOPEE_API_KEY}`. The values are never in the config.
5. **Hands the key to you.** It tells you where to copy the project UUID and generate a key in Commander, and where to put them: your shell environment, a git-ignored `.env` file or your editor's secret prompt. Then you restart or reload the agent.
6. **Checks the connection.** It calls `wopee_fetch_test_inventory`, which only reads, and reports how many analyses and test cases your project has. A new project with zero tests counts as a success.
7. **Offers one test run.** Runs use Wopee.io's cloud runners and your plan, so it starts one only after you say yes. See [Your first test from your coding agent](../guides/wopee-mcp/first-test.md).
8. **Reports.** A short summary: what changed, where the key lives, the check result and how to undo the setup.

## What it changes

| Client | File it writes | Where the key lives |
| --- | --- | --- |
| Claude Code | `.mcp.json` in the repository (`claude mcp add --scope project`), or `~/.claude.json` with user scope | The environment you start `claude` from |
| Cursor | `.cursor/mcp.json`, or `~/.cursor/mcp.json` | A git-ignored `.env` file (`envFile`) or the environment (`${env:...}`) |
| GitHub Copilot in VS Code | `.vscode/mcp.json` | A git-ignored `.env` file (`envFile`) or VS Code's secret prompt (`inputs`) |
| OpenAI Codex | `~/.codex/config.toml` | The environment Codex starts from (`env_vars`) |
| Other MCP clients | The client's MCP config file | The client's reference syntax, or the value in a user-level file outside your repository |

Only with your OK, it also:

- adds `.env` to `.gitignore` and writes `.env` with **empty** `WOPEE_API_KEY=` and `WOPEE_PROJECT_UUID=` lines for you to fill in;
- adds a short "Testing with Wopee.io" section to your agent instructions file (`AGENTS.md`, `CLAUDE.md`, `.github/copilot-instructions.md` or a Cursor rule).

It never:

- asks for the API key in the chat or writes it into a committed file;
- uses `sudo`, pipes a download into a shell (`curl | bash`), installs with `--yes`, edits your shell profile or turns off TLS checks;
- starts an analysis or a test run without your yes;
- contacts hosts other than wopee.io, docs.wopee.io, cmd.wopee.io and the npm registry.

## Your API key stays out of the chat

- **Type the key yourself**, in your terminal, your `.env` file or your editor's secret prompt. Chat history is stored, so a key in the chat is a key in a transcript.
- **Pasted it anyway?** Generate a new key in Commander and delete the pasted one under **Existing keys**. See [Rotate a key](../guides/api-keys.md#rotate-a-key).
- **The key acts as you.** It works for one project, with the rights of the user who created it, and runs count toward that user's plan. Treat it like a password.
- **The config holds references only**, so you can commit `.mcp.json`, `.vscode/mcp.json` or `.cursor/mcp.json`. Each teammate generates their own key.
- **What leaves your machine:** only the arguments of the tool calls your agent makes. The server does not read your repository.

## Set it up by hand

Rather do it yourself? Get the key and project UUID ([how](../guides/api-keys.md)), put them into your environment, then add the server for your client.

### Claude Code

```shell
claude mcp add --scope project wopee -e 'WOPEE_API_KEY=${WOPEE_API_KEY}' -e 'WOPEE_PROJECT_UUID=${WOPEE_PROJECT_UUID}' -- npx -y wopee-mcp
```

Keep the single quotes, so `.mcp.json` stores the references, not the values. Details: [Claude Code](../guides/wopee-mcp/claude-code.md).

### Cursor

```json title=".cursor/mcp.json"
{
  "mcpServers": {
    "wopee": {
      "command": "npx",
      "args": ["-y", "wopee-mcp"],
      "envFile": "${workspaceFolder}/.env"
    }
  }
}
```

Then switch the server on in **Customize** › **MCPs**; project servers start disabled. Details: [Cursor](../guides/wopee-mcp/cursor.md).

### GitHub Copilot in VS Code

```json title=".vscode/mcp.json"
{
  "servers": {
    "wopee": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "wopee-mcp"],
      "envFile": "${workspaceFolder}/.env"
    }
  }
}
```

Click **Start** above the entry. Details, Copilot CLI and the cloud agent: [GitHub Copilot](../guides/wopee-mcp/github-copilot.md).

### OpenAI Codex

```toml title="~/.codex/config.toml"
[mcp_servers.wopee]
command = "npx"
args = ["-y", "wopee-mcp"]
env_vars = ["WOPEE_API_KEY", "WOPEE_PROJECT_UUID"]
```

Details: [OpenAI Codex](../guides/wopee-mcp/codex.md).

### Other clients

Use the [universal configuration](../guides/wopee-mcp/index.md#universal-configuration), or the guide for [OpenCode](../guides/wopee-mcp/opencode.md), [Antigravity and Gemini CLI](../guides/wopee-mcp/antigravity.md), [JetBrains](../guides/wopee-mcp/jetbrains.md), [Devin Desktop](../guides/wopee-mcp/devin-desktop-windsurf.md), [Visual Studio](../guides/wopee-mcp/visual-studio.md) or [other MCP clients](../guides/wopee-mcp/other-clients.md).

Then restart the agent and ask:

```text
How many tests do I have in Wopee.io, and which ones have never run?
```

## Undo

- **Claude Code:** `claude mcp remove wopee --scope project` (or `--scope user`).
- **OpenAI Codex:** delete the `[mcp_servers.wopee]` table from `~/.codex/config.toml`.
- **Other clients:** delete the `wopee` entry from the config file.
- Then delete the key in Commander under **More** › **Settings** › **API Keys** › **Existing keys**.

## Next

- [Your first test from your coding agent](../guides/wopee-mcp/first-test.md): from the first question to a verdict, with sample outputs
- [Troubleshooting](../guides/wopee-mcp/troubleshooting.md): every error message and its fix
- [Wopee.io MCP server](../guides/wopee-mcp/index.md): all 15 tools, prompts and how runs work
