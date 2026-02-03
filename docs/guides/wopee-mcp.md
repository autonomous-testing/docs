# 🚀 Wopee.io MCP

A Model Context Protocol (MCP) server for integrating with Wopee.io's autonomous testing platform. Manage analysis suites, generate test cases and user stories, and dispatch autonomous testing agents directly from your IDE.

!!! info "Full Documentation"

    This is a simplified overview. For complete documentation, examples, and advanced usage, see the [full README on npmjs.com](https://www.npmjs.com/package/wopee-mcp?activeTab=readme).

## Quick Start

### Prerequisites

- Node.js 18+
- An MCP-compatible IDE (Cursor, VS Code, etc.)
- A Wopee API key from [cmd.wopee.io](https://cmd.wopee.io)

### Installation

**One-Click (VS Code / Cursor):**

1. `Ctrl+Shift+P` → "MCP: Install Server"
2. Enter: `wopee-mcp`
3. Configure environment variables

**Manual:**

```bash
npm install -g wopee-mcp
```

### Configuration

Add to your MCP configuration:

```json
{
  "mcpServers": {
    "wopee": {
      "command": "npx wopee-mcp",
      "env": {
        "WOPEE_PROJECT_UUID": "your-project-uuid-here",
        "WOPEE_API_KEY": "your-api-key-here"
      }
    }
  }
}
```

**Required Environment Variables:**

| Variable             | Description                                            |
| -------------------- | ------------------------------------------------------ |
| `WOPEE_PROJECT_UUID` | Your Wopee project UUID                                |
| `WOPEE_API_KEY`      | Your API key from [cmd.wopee.io](https://cmd.wopee.io) |

**Optional:** For corporate proxy configuration, add `HTTPS_PROXY` to the env section.

## Getting Started

Most tools require a `suiteUuid`. Start by getting or creating a suite:

**Option 1: Use Existing Suites**

```
Fetch all existing analysis suites for my project
```

**Option 2: Create a New Suite**

- **Automatic Analysis:** `Dispatch a new analysis suite` - Creates and runs full analysis/crawling
- **Blank Suite:** `Create a blank analysis suite` - Creates an empty suite for manual configuration

## Available Tools

| Tool                          | Purpose             | Example Prompt                            |
| ----------------------------- | ------------------- | ----------------------------------------- |
| `wopee_fetch_analysis_suites` | List all suites     | `Fetch all analysis suites`               |
| `wopee_dispatch_analysis`     | Start full analysis | `Dispatch a new analysis suite`           |
| `wopee_create_blank_suite`    | Create empty suite  | `Create a blank analysis suite`           |
| `wopee_generate_artifact`     | Generate artifacts  | `Generate app context for my suite`       |
| `wopee_fetch_artifact`        | Retrieve artifacts  | `Fetch user stories for the latest suite` |
| `wopee_update_artifact`       | Update artifacts    | `Update app context with this content`    |
| `wopee_dispatch_agent`        | Execute tests       | `Dispatch agent for US001 TC003`          |

### Artifact Types

**For `wopee_generate_artifact`:**

- `APP_CONTEXT`, `GENERAL_USER_STORIES`, `USER_STORIES_WITH_TEST_CASES`
- `TEST_CASES`, `TEST_CASE_STEPS`, `REUSABLE_TEST_CASES`, `REUSABLE_TEST_CASE_STEPS`

**For `wopee_fetch_artifact` / `wopee_update_artifact`:**

- `APP_CONTEXT`, `GENERAL_USER_STORIES`, `USER_STORIES`, `PLAYWRIGHT_CODE`, `PROJECT_CONTEXT`

## Typical Workflow

1. **Get a suite:** Fetch existing suites or create a new one
2. **Generate artifacts:** App context → User stories → Test cases → Test steps
3. **Fetch content:** Retrieve generated artifacts as needed
4. **Run tests:** Dispatch agent to execute test cases

## Troubleshooting

| Issue              | Solution                                       |
| ------------------ | ---------------------------------------------- |
| Command not found  | Run `npm install -g wopee-mcp`                 |
| API key error      | Check environment variables                    |
| Connection timeout | Configure `HTTPS_PROXY` for corporate networks |
| Tools not showing  | Restart your editor                            |

!!! tip "Visual Interface"

    Use [cmd.wopee.io](https://cmd.wopee.io) for a convenient visual representation of generated data and agent run results.

!!! note "Early Preview"

    This package is in early preview. Features and functionalities may change.
