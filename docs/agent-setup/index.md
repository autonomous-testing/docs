---
title: Set up Wopee.io with your coding agent
description: Set up Wopee.io testing for a repository with one command, npx -y @wopee-io/init@latest, run by you or your coding agent (Claude Code, Cursor, GitHub Copilot, Codex or OpenCode). You approve in Commander, and the Wopee.io MCP server is connected without the API key ever reaching the chat. What it does and changes, prerequisites and manual setup.
type: How-to
updated: 19 November 2026
---

# Set up Wopee.io with your coding agent

Setting up Wopee.io testing for a repository takes one command, run from the repository root:

```shell
npx -y @wopee-io/init@latest
```

Ask your coding agent to set up Wopee.io testing for the repository and it can run the command itself: the command asks no questions and needs no key. It prints a link and three pairing words. You approve in Commander, and the command connects the [Wopee.io MCP server](../guides/wopee-mcp/index.md) to your project with a new API key that neither you nor the agent has to copy. The API key never passes through the chat.

For a guided setup, paste the line below instead. The agent then checks the connection with a read-only call and offers to run one test. It shows its plan first and asks before it changes anything.

!!! tip wo-agent-setup "Paste this into your coding agent"

    ```text
    Set me up for Wopee.io: follow https://wopee.io/agent-setup/prompt.md, show me the plan first, and ask before changing anything.
    ```

    The instructions are plain Markdown on our own domain. Read them before you paste: [wopee.io/agent-setup/prompt.md](https://wopee.io/agent-setup/prompt.md){: target="\_blank"}.

The command configures Claude Code, Cursor, GitHub Copilot in VS Code, OpenAI Codex and OpenCode. For other MCP clients the instructions add one universal entry instead.

## Before you start

- **Node.js 20.18.1 or newer.** The command and the server run with `npx`. The agent checks the version and never installs Node.js for you.
- **A Wopee.io project with your app's URL.** No account yet? Sign up with your app's URL, and Commander creates the project and starts the first analysis for you:

    ```text
    https://cmd.wopee.io/signup?url=<your-app-url>
    ```

    The app must be reachable from the internet, because the tests run on Wopee.io's cloud runners. `localhost` does not work: [expose it with a tunnel or use a deployed URL](../guides/test-localhost.md).

- **Project admin rights.** Only project admins can approve the pairing, because it creates a project API key. See [Find your API key and project UUID](../guides/api-keys.md).
- **An agent that runs local (stdio) MCP servers.** Web-only chat apps cannot use the server.

## What the agent does

1. **Checks for an existing setup.** If the `wopee` tools already work, it skips to the check in step 6. Running the line again is safe.
2. **Detects your setup and shows a plan.** It works out the client, the operating system and the repository, then lists what will change and waits for your yes.
3. **Checks Node.js.** `node --version` only reads. New to Wopee.io? It gives you the sign-up link first, because the pairing needs a project you administer.
4. **Runs `npx -y @wopee-io/init@latest`.** The command returns within seconds with a link and three words, for example `brave-otter-42`. The agent shows you both, then runs `npx -y @wopee-io/init@latest --resume`, which waits about 90 seconds for your approval.
5. **You approve in Commander.** Check that the words match, pick the project and click **Approve**. A new, named API key goes back to the waiting command, encrypted to it, and the command writes the files. If you take longer than about 90 seconds, the agent runs `--resume` again once you say you approved. Then you restart or reload the agent.
6. **Checks the connection.** It calls `wopee_setup_check` (or `wopee_fetch_test_inventory`), which only reads, and reports your project with its analyses and test cases. A new project with zero tests counts as a success.
7. **Offers one test run.** Runs use Wopee.io's cloud runners and your plan, so it starts one only after you say yes. See [Your first test from your coding agent](../guides/wopee-mcp/first-test.md).
8. **Reports.** A short summary: what changed, where the key lives, the check result and how to undo the setup.

## What it changes

The command writes `WOPEE_API_KEY` and `WOPEE_PROJECT_UUID` to `.env` (or to `.env.local` when the repository has one), adds that file to `.gitignore`, and adds one MCP server entry named `wopee` with **no key in it**. `wopee-mcp` reads the key from the env file itself.

| Client | File it writes |
| --- | --- |
| Claude Code | `.mcp.json` in the repository |
| Cursor | `.cursor/mcp.json` |
| GitHub Copilot in VS Code | `.vscode/mcp.json` |
| OpenCode | `opencode.json` |
| OpenAI Codex | `~/.codex/config.toml` (Codex reads project config only in trusted projects) |
| Other MCP clients | One entry in the client's MCP config file, added by the agent; you type the values into `.env` |

It keeps other servers and comments in these files, never overwrites a different `wopee` entry without asking, and refuses to write the key into an env file that git tracks. In Commander, the key is listed as `wopee-init · <agent> · <machine> · <date>`.

It never:

- asks for the API key in the chat, reads your `.env` file or writes the key into a committed file;
- uses `sudo`, pipes a download into a shell (`curl | bash`), installs with `--yes`, edits your shell profile or turns off TLS checks;
- starts an analysis or a test run without your yes;
- contacts hosts other than wopee.io, docs.wopee.io, cmd.wopee.io, api.wopee.io and the npm registry.

## Your API key stays out of the chat

- **Nobody copies the key.** It travels from the api to the waiting command, encrypted to a one-time key the command made, and the command writes it straight to the git-ignored env file. No line the command prints contains it. Chat history is stored, so a key in the chat is a key in a transcript.
- **Pasted it anyway?** Generate a new key in Commander and delete the pasted one under **Existing keys**. See [Rotate a key](../guides/api-keys.md#rotate-a-key).
- **The key acts as you.** It works for one project, with the rights of the user who created it, and runs count toward that user's plan. Treat it like a password.
- **The config holds no key**, so you can commit `.mcp.json`, `.vscode/mcp.json`, `.cursor/mcp.json` or `opencode.json`. Each teammate runs the command and gets their own key.
- **What leaves your machine:** only the arguments of the tool calls your agent makes. The server does not read your repository.

## Set it up by hand

Rather do it yourself? Run the same command in your terminal, from the repository:

```shell
npx -y @wopee-io/init@latest
```

It opens the approval page in your browser and asks which agents to configure. Your Wopee.io instance has no pairing yet, or you prefer to paste a key? `npx -y @wopee-io/init@latest --manual` asks for the project UUID and a key ([where to find them](../guides/api-keys.md)) in a hidden prompt and writes the same files. All options: [@wopee-io/init on npm](https://www.npmjs.com/package/@wopee-io/init){: target="\_blank"}.

Or add the server for your client yourself, with the values in your environment:

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
- Remove the `WOPEE_*` lines from `.env`.
- Then delete the key in Commander under **More** › **Settings** › **API Keys** › **Existing keys**.

## Next

- [Your first test from your coding agent](../guides/wopee-mcp/first-test.md): from the first question to a verdict, with sample outputs
- [Troubleshooting](../guides/wopee-mcp/troubleshooting.md): every error message and its fix
- [Wopee.io MCP server](../guides/wopee-mcp/index.md): all 15 tools, prompts and how runs work
