# 🚀 Wopee.io MCP

(early preview)

## Overview

Wopee.io MCP is a Model Context Protocol server for integrating with the Wopee testing platform. This server provides tools for managing analysis suites, generating test cases, user stories, and dispatching autonomous testing agents.

Now, you can use Wopee.io MCP to integrate with your favorite IDE and use Wopee.io AI Agents to increase your productivity and speed up your testing while developing your web app.

## Features

- **Dispatch Analysis**: Start analysis of web applications to understand their structure and behavior
- **Dispatch Agent**: Execute tests for specific suites with autonomous testing agents
- **Generate Artifacts**: Create app context, user stories, test cases, and more from analysis results
- **Fetch Artifacts**: Retrieve existing app context, user stories, test cases, and Playwright code
- **Update Artifacts**: Modify existing artifacts for a specific suite
- **Fetch Analysis Suites**: Fetch all analysis suites for a project

## Quick Start Guide

### 🚀 One-Click Installation

**For VS Code / Cursor:**

1. `Ctrl+Shift+P` → "MCP: Install Server"
2. Enter: `wopee-mcp`
3. Configure your environment variables in the MCP config

### 🛠 Available Tools

| Tool                          | Purpose                   | Example                                                                     |
| ----------------------------- | ------------------------- | --------------------------------------------------------------------------- |
| `wopee_fetch_analysis_suites` | Fetch all analysis suites | `Fetch all existing analysis suites for my project`                         |
| `wopee_dispatch_analysis`     | Start app analysis        | `Dispatch a new analysis suite`                                             |
| `wopee_generate_artifact`     | Generate artifacts        | `Generate app context for my most recent analysis suite`                    |
| `wopee_fetch_artifact`        | Fetch existing artifacts  | `Fetch user stories for the latest suite`                                   |
| `wopee_update_artifact`       | Update existing artifacts | `Update app context file for the most recent suite`                         |
| `wopee_dispatch_agent`        | Execute tests             | `Dispatch agent for my latest suite's user story US001 and test case TC003` |

### 🔧 Manual Installation

```bash
npm install -g wopee-mcp
```

### ⚙️ Configuration

Add the Wopee MCP server to your MCP configuration:

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

### Prerequisites

Before using the Wopee MCP server, ensure you have:

1. **VS Code** with the MCP extension installed, or **Cursor** ... or even could be used with ChatGPT or Claude or any other AI agent that supports MCP.
2. A **Wopee API key** from [cmd.wopee.io](https://cmd.wopee.io) (in your project's settings)
3. **Node.js 18+** installed on your system

## Configuration

### Environment Variables

#### Required Environment Variables

- **`WOPEE_PROJECT_UUID`** - Your Wopee project UUID. This identifies which project you're working with.
- **`WOPEE_API_KEY`** - Your Wopee API key. You can create one at [cmd.wopee.io](https://cmd.wopee.io), in your project's settings.

#### Optional Environment Variables

- **`WOPEE_API_URL`** - The Wopee API endpoint URL. Should be specified only for testing/development purposes.

### Corporate Proxy Configuration

If you're behind a corporate proxy/VPN and experiencing connection timeouts, you can configure proxy settings using standard environment variables:

```json
{
  "mcpServers": {
    "wopee": {
      "command": "npx wopee-mcp",
      "env": {
        "WOPEE_PROJECT_UUID": "your-project-uuid-here",
        "WOPEE_API_KEY": "your-api-key-here",
        "HTTPS_PROXY": "http://your-proxy-server:8080"
      }
    }
  }
}
```

#### Supported Proxy Environment Variables

- **`HTTPS_PROXY`** or **`https_proxy`** - Proxy server URL for HTTPS connections (recommended)
- **`HTTP_PROXY`** or **`http_proxy`** - Fallback proxy server URL

#### Finding Your Proxy Settings

If you're unsure about your proxy settings, check your VS Code settings (`settings.json`) for `http.proxy` value, or consult your IT department. Common corporate proxy formats:

- `http://proxy.company.com:8080`
- `http://10.x.x.x:8080`
- `http://username:password@proxy.company.com:8080` (if authentication is required)

## Getting Started

Most tools in this MCP server require a `suiteUuid` to operate. You have two options to get started:

### Option 1: Use Existing Suites

Start by fetching your existing analysis suites:

```
Use the wopee_fetch_analysis_suites tool to retrieve all available suites for your project.
```

This will return a list of all analysis suites with their UUIDs, which you can then use with other tools.

### Option 2: Create a New Suite

If you don't have any suites yet, create a fresh analysis suite:

```
Use the wopee_dispatch_analysis tool to create and dispatch a new analysis/crawling suite.
```

This will create a new suite and return its UUID, which you can use for subsequent operations.

## Usage

Once configured, you can use the Wopee tools in your chat interface. Simply describe what you want to do in natural language.

### Quick Examples

**Fetch Analysis Suites:**

```
Fetch all existing analysis suites for my project
```

**Start Analysis:**

```
Dispatch a new analysis suite
```

**Generate Artifacts:**

```
Generate app context for my most recent analysis suite
```

**Execute Tests:**

```
Dispatch agent for my latest suite's user story US001 and test case TC003
```

## Real-World Usage Examples

### Complete Testing Workflow

Here's a typical workflow from analysis to test execution:

#### 1. Start Analysis

```
Dispatch analysis
```

#### 2. Generate Application Context

```
Generate app context
```

#### 3. Create User Stories

```
Generate user stories with test cases
```

#### 4. Generate Test Case Steps

```
Generate test case steps
```

#### 5. Review Generated Tests

```
Give me all the generated tests in tabular format
```

#### 6. Execute Tests

```
Dispatch agent to run test TC001 from US001
```

### Advanced Usage Examples

#### Multi-Language Support

```
Generate user stories with additional instructions: "All outputs has to be in Portuguese language"
```

```
Generate test cases with additional instructions: "Focus on fields validations, make sure to test all fields. Use USD and EUR currencies. Focus on payment flows."
```

#### Custom Analysis Instructions

```
Dispatch analysis with additional instructions: "All outputs has to be in Czech Language"
```

```
Generate test cases with focus on security testing like password validation, email validation, etc.
```

### Data Retrieval Examples

#### Check Analysis Status

```
What is the status of my analysis?
```

```
Show me all available analysis suites
```

#### Get Specific Test Cases

```
Give me all tests from the A001
```

```
Show me test cases from analysis A007
```

#### View User Stories

```
Give me a list of the user stories in bullet points format
```

```
Give me the same table with the user stories but also provide a column with number of tests per story
```

### Test Execution Examples

#### Run Specific Tests

```
Dispatch all tests for user story US001
```

```
Dispatch agent to run all tests for user story US001
```

#### Monitor Execution

```
What about now?
```

```
What are the current test execution results?
```

## Common Workflows

### 1. New Project Setup

1. **Dispatch analysis** for your application
2. **Generate app context** to understand the application
3. **Generate general user stories** for high-level overview
4. **Generate user stories with test cases** based on analysis
5. **Generate test case steps** for detailed test execution
6. **Review and organize** the generated content

### 2. Test Execution Workflow

1. **Check available tests** in your analysis
2. **Select specific tests** to execute
3. **Dispatch agent** to run selected tests
4. **Monitor execution status** and results
5. **Review test outcomes** and iterate

### 3. Multi-Analysis Comparison

1. **Fetch all analysis suites** for your project
2. **Compare test cases** from different analyses
3. **Check statuses** of all analyses
4. **Select best performing** analysis for execution

## Tips and Best Practices

### 1. Use Descriptive Analysis Names

- Include the application name and version
- Add date or iteration information
- Example: `"E-commerce App v2.1 - Payment Testing"`

### 2. Provide Clear Instructions

- Be specific about language requirements
- Include focus areas for testing
- Example: `"Focus on user authentication and payment flows"`

### 3. Monitor Progress

- Check analysis status regularly
- Wait for completion before proceeding
- Use status queries to track progress

### 4. Organize by Analysis

- Keep related tests in the same analysis
- Use consistent naming conventions
- Document analysis purposes

### 5. Test Execution

- Start with single test cases
- Monitor execution status
- Scale up to multiple tests once stable

## Available Tools

### Suite Management

#### wopee_fetch_analysis_suites

Fetches all analysis suites for your project. This is a good starting point to see what suites are available.

- **Returns:** Array of analysis suites with their UUIDs, names, statuses, and metadata

**Example Usage:**

```
Fetch all existing analysis suites for my project
```

#### wopee_dispatch_analysis

Creates and dispatches a new analysis/crawling suite for your project. Use this to start a fresh analysis session.

- **Returns:** Success message with the created suite information

**Example Usage:**

```
Dispatch a new analysis suite
```

### Generation Tools

These tools generate various artifacts for a specific suite. All require a `suiteUuid` and `type` to generate.

#### wopee_generate_artifact

Generates a specific file (artifact) for the selected suite.

**Parameters:**

- `suiteUuid` (string, required): The UUID of the suite
- `type` (string, required): One of:
  - `APP_CONTEXT` - Application context markdown
  - `GENERAL_USER_STORIES` - High-level user stories
  - `USER_STORIES_WITH_TEST_CASES` - Detailed user stories with test cases
  - `TEST_CASES` - Comprehensive test cases
  - `TEST_CASE_STEPS` - Detailed test case steps
  - `REUSABLE_TEST_CASES` - Reusable test case templates
  - `REUSABLE_TEST_CASE_STEPS` - Reusable test case step templates

**Example Usage:**

```
Generate app context for my most recent analysis suite
```

### Fetch Tools

These tools retrieve generated artifacts for a specific suite. All require a `suiteUuid` and `type`.

#### wopee_fetch_artifact

Fetches the enquired file (artifact) from the selected suite.

**Parameters:**

- `suiteUuid` (string, required): The UUID of the suite
- `type` (string, required): One of:
  - `APP_CONTEXT` - Application context markdown
  - `GENERAL_USER_STORIES` - General user stories markdown
  - `USER_STORIES` - Detailed user stories JSON
  - `PLAYWRIGHT_CODE` - Generated Playwright test code
  - `PROJECT_CONTEXT` - Project context markdown
- `identifier` (string, optional): Identifier of the test case to fetch Playwright code for, e.g., `US003:TC004`. Required only for `PLAYWRIGHT_CODE` type.

**Example Usage:**

```
Fetch user stories for the latest suite
```

```
Fetch Playwright code for test case US004:TC006
```

### Update Tools

These tools are used to update or set certain files (artifacts) for a specific suite.

#### wopee_update_artifact

Updates/replaces existing file (artifact) for a specific suite.

**Parameters:**

- `suiteUuid` (string, required): The UUID of the suite
- `type` (string, required): One of:
  - `APP_CONTEXT` - Application context markdown
  - `GENERAL_USER_STORIES` - General user stories markdown
  - `USER_STORIES` - Detailed user stories JSON
  - `PLAYWRIGHT_CODE` - Generated Playwright test code
  - `PROJECT_CONTEXT` - Project context markdown
- `content` (string, required): Markdown content for `APP_CONTEXT`, `GENERAL_USER_STORIES` and `PROJECT_CONTEXT`, structured JSON for `USER_STORIES`
- `identifier` (string, optional): Identifier of the test case to update Playwright code for, e.g., `US003:TC004`. Required only for `PLAYWRIGHT_CODE` type.

**Example Usage:**

```
Update app context file for the most recent suite with this content: <YourMarkdown>
```

### Agent Testing

#### wopee_dispatch_agent

Dispatches an autonomous testing agent to execute test cases for a selected suite.

**Parameters:**

- `suiteUuid` (string, required): The UUID of the suite containing the test cases
- `analysisIdentifier` (string, required): The analysis identifier for the suite
- `testCases` (array, required): Array of test case objects to execute, each containing:
  - `testCaseId` (string): The ID of the test case (e.g., `TC001`)
  - `userStoryId` (string): The ID of the associated user story (e.g., `US001`)

**Example Usage:**

```
Dispatch agent for my latest suite's user story US001 and test case TC003
```

## Typical Workflow

1. **Start with a suite:**

   - Use `wopee_fetch_analysis_suites` to see existing suites, OR
   - Use `wopee_dispatch_analysis` to create a new suite

2. **Generate artifacts:**

   - Generate app context: `wopee_generate_artifact` with `APP_CONTEXT`
   - Generate general user stories: `wopee_generate_artifact` with `GENERAL_USER_STORIES`
   - Generate user stories with test cases: `wopee_generate_artifact` with `USER_STORIES_WITH_TEST_CASES`
   - Generate reusable test cases: `wopee_generate_artifact` with `REUSABLE_TEST_CASES`
   - Generate reusable test case steps: `wopee_generate_artifact` with `REUSABLE_TEST_CASE_STEPS`
   - Generate test case steps: `wopee_generate_artifact` with `TEST_CASE_STEPS`

3. **Fetch generated content:**

   - Use `wopee_fetch_artifact` to retrieve generated markdown/JSON files

4. **Run tests:**
   - Use `wopee_dispatch_agent` to execute test cases with the autonomous testing agent

## Notes

- Most tools require a `suiteUuid`. Always start by fetching or creating a suite.
- `wopee_dispatch_analysis` tool will go through the whole cycle of processing - crawling the application and generating all of the files (artifacts) one by one.
- It is advisable to use [cmd.wopee.io](https://cmd.wopee.io) for a convenient visual representation of the generated data and results of the agent runs.

## Example Session Flow

Here's a complete example session showing the typical workflow:

```
User: Dispatch analysis

Assistant: ✅ Analysis successfully dispatched! Analysis UUID: 008ccdd2-91a3-432e-8086-020bf337eaa7

User: Generate app context

Assistant: ✅ App context generated successfully!

User: Generate user stories

Assistant: ✅ User stories generated successfully!

User: Give me all the generated tests in tabular format

Assistant: 📊 Here are all your generated test cases...

User: Dispatch agent to run test TC001 from US001

Assistant: ✅ Test execution started successfully!
```

## 🆘 Troubleshooting

### Common Issues

- **Command not found**: Run `npm install -g wopee-mcp`
- **API key error**: Check environment variables in MCP config
- **Connection failed**: Verify internet and API key
- **Connection timeout**: Configure corporate proxy settings
- **Tools not showing**: Restart editor

### Error Handling

#### Common Error Messages

1. **"User not found" error:**

   - Check API key configuration
   - Verify project permissions
   - Contact support if persistent

2. **"Analysis not found" error:**

   - Verify suite UUID
   - Check analysis completion status
   - Ensure analysis exists

3. **"Test execution failed" error:**
   - Check test case validity
   - Verify application accessibility
   - Review test steps

### Getting Help

- **Check logs**: Look in the MCP server output panel
- **Verify installation**: Run `wopee-mcp --help` in terminal
- **Test connection**: Use the `wopee_dispatch_analysis` tool

!!! note "Need help?"

    For support and further information, please refer to the [npm package page](https://www.npmjs.com/package/wopee-mcp) or contact the package maintainers.

_Note: This package is currently in early preview; features and functionalities are subject to change._
