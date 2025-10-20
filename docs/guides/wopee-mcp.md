# 🚀 Wopee.io MCP

(early preview)

## Overview

Wopee.io MCP is a Model Context Protocol server for integrating with the Wopee testing platform. This server provides tools for dispatching analysis, generating app context, user stories, test cases, and running test executions.

Now, you can use Wopee.io MCP to integrate with your favorite IDE and use Wopee.io AI Agents to increase your productivity and speed up your testing while developing your web app.

## Features

- **Dispatch Analysis**: Start analysis of web applications to understand their structure and behavior
- **Dispatch Agent**: Execute tests for specific projects and suites
- **Generate App Context**: Create detailed application context based on analysis results
- **Generate General User Stories**: Generate high-level user stories from analysis data
- **Generate User Stories**: Generate detailed user stories and acceptance criteria from analysis data
- **Generate Test Cases**: Generate comprehensive test cases from analysis and user stories
- **Get App Context**: Retrieve existing app context for a project and suite
- **Get User Stories**: Retrieve existing user stories for a project and suite
- **Get Test Cases**: Retrieve existing test cases for a project and suite
- **Fetch Analysis Suites**: Fetch all analysis suites for a project

## Quick Start Guide

### 🚀 One-Click Installation

**For VS Code / Cursor:**
1. `Ctrl+Shift+P` → "MCP: Install Server"
2. Enter: `wopee-mcp`
3. Add your API key into .env file

### 🛠 Available Tools

| Tool | Purpose | Example |
|------|---------|---------|
| `wopee_dispatch_analysis` | Start app analysis | `@wopee wopee_dispatch_analysis Project UUID: project-123` |
| `wopee_dispatch_agent` | Execute tests | `@wopee wopee_dispatch_agent Project UUID: project-123 Suite UUID: suite-123` |
| `wopee_generate_app_context` | Generate app context | `@wopee wopee_generate_app_context Project UUID: project-123 Suite UUID: suite-123` |
| `wopee_generate_general_user_stories` | Generate general user stories | `@wopee wopee_generate_general_user_stories Project UUID: project-123 Suite UUID: suite-123` |
| `wopee_generate_user_stories` | Generate detailed user stories | `@wopee wopee_generate_user_stories Project UUID: project-123 Suite UUID: suite-123` |
| `wopee_generate_test_cases` | Generate test cases | `@wopee wopee_generate_test_cases Project UUID: project-123 Suite UUID: suite-123` |
| `wopee_get_app_context` | Get existing app context | `@wopee wopee_get_app_context Project UUID: project-123 Suite UUID: suite-123` |
| `wopee_get_user_stories` | Get existing user stories | `@wopee wopee_get_user_stories Project UUID: project-123 Suite UUID: suite-123` |
| `wopee_get_test_cases` | Get existing test cases | `@wopee wopee_get_test_cases Project UUID: project-123 Suite UUID: suite-123` |
| `wopee_fetch_analysis_suites` | Fetch all analysis suites | `@wopee wopee_fetch_analysis_suites Project UUID: project-123` |

### 🔧 Manual Installation

```bash
npm install -g wopee-mcp
```

### ⚙️ Configuration

Set environment variables:
```bash
export WOPEE_API_KEY=your_api_key_here
export WOPEE_PROJECT_UUID=your_project_uuid_here
```

### Prerequisites

Before using the Wopee MCP server, ensure you have:

1. **VS Code** with the MCP extension installed, or **Cursor** ... or even could be used with ChatGPT or Claude or any other AI agent that supports MCP.
2. A **Wopee API key** from [wopee.io](https://wopee.io)
3. **Node.js 18+** installed on your system

## Configuration

The server loads configuration from a `.env` file in the project root directory (where `package.json` is located).

### Environment Variables

- `WOPEE_API_KEY` (required): Your Wopee API key
- `WOPEE_PROJECT_UUID` (required): Your Wopee project UUID
- `WOPEE_API_URL` (optional): Wopee API endpoint (defaults to `https://api.wopee.io/`)

### Setting up .env file

1. **Copy the example file:**
   ```bash
   cp env.example .env
   ```

2. **Edit the .env file in the project root:**
   ```bash
   # Wopee API Configuration
   WOPEE_API_KEY=your_actual_api_key_here
   WOPEE_PROJECT_UUID=your_project_uuid_here
   WOPEE_API_URL=https://api.dev.wopee.io/
   ```

3. **For MCP integration, update your `mcp.json`:**
   ```json
   {
     "mcpServers": {
       "wopee": {
         "command": "npx",
         "args": ["wopee-mcp@latest"],
         "env": {}
       }
     }
   }
   ```

   **Note:** The server automatically loads API keys from the `.env` file in the project root. No need to hardcode them in the MCP configuration.

## Usage

Once configured, you can use the Wopee tools in your chat interface. Simply type `@wopee` followed by the tool name and required parameters.

### Quick Examples

**Start Analysis:**
```
@wopee wopee_dispatch_analysis Project UUID: project-123
```

**Generate Test Cases:**
```
@wopee wopee_generate_test_cases Project UUID: project-123 Suite UUID: suite-123
```

**Execute Tests:**
```
@wopee wopee_dispatch_agent Project UUID: project-123 Suite UUID: suite-123
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
Generate user stories
```

#### 4. Generate Test Cases
```
Generate test cases
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
3. **Generate user stories** based on analysis
4. **Generate test cases** from user stories
5. **Review and organize** the generated content

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

### 1. wopee_dispatch_analysis

Start a new analysis for a given URL.

**Parameters:**
- `projectUuid` (string, required): UUID of the project
- `iterations` (number, required): Number of analysis iterations
- `suiteAnalysisConfig` (object, required): Configuration for the analysis

**Example:**
```json
{
  "projectUuid": "project-123",
  "iterations": 5,
  "suiteAnalysisConfig": {
    "startingUrl": "https://example.com",
    "username": "testuser",
    "password": "testpass",
    "cookiesPreference": "ACCEPT_ALL"
  }
}
```

### 2. wopee_dispatch_agent

Execute tests for specific projects and suites.

**Parameters:**
- `projectUuid` (string, required): UUID of the project
- `suiteUuid` (string, required): UUID of the test suite
- `analysisIdentifier` (string, required): Analysis identifier
- `testCases` (array, required): Array of test cases to execute

**Example:**
```json
{
  "projectUuid": "project-123",
  "suiteUuid": "suite-123",
  "analysisIdentifier": "analysis-123",
  "testCases": [
    {
      "testCaseId": "test-1",
      "userStoryId": "story-1"
    }
  ]
}
```

### 3. wopee_generate_app_context

Generate application context based on analysis results.

**Parameters:**
- `projectUuid` (string, required): UUID of the project
- `suiteUuid` (string, required): UUID of the test suite
- `extraPrompt` (string, optional): Optional prompt to modify the app context generation

**Example:**
```json
{
  "projectUuid": "project-123",
  "suiteUuid": "suite-123",
  "extraPrompt": "Focus on user authentication flows"
}
```

### 4. wopee_generate_general_user_stories

Generate high-level user stories from analysis data.

**Parameters:**
- `projectUuid` (string, required): UUID of the project
- `suiteUuid` (string, required): UUID of the test suite
- `extraPrompt` (string, optional): Optional prompt to modify the user story generation

**Example:**
```json
{
  "projectUuid": "project-123",
  "suiteUuid": "suite-123",
  "extraPrompt": "Include high-level business requirements"
}
```

### 5. wopee_generate_user_stories

Generate detailed user stories and acceptance criteria from analysis data.

**Parameters:**
- `projectUuid` (string, required): UUID of the project
- `suiteUuid` (string, required): UUID of the test suite
- `extraPrompt` (string, optional): Optional prompt to modify the user story generation

**Example:**
```json
{
  "projectUuid": "project-123",
  "suiteUuid": "suite-123",
  "extraPrompt": "Include edge cases and error scenarios"
}
```

### 6. wopee_generate_test_cases

Generate comprehensive test cases from analysis and user stories.

**Parameters:**
- `projectUuid` (string, required): UUID of the project
- `suiteUuid` (string, required): UUID of the test suite
- `extraPrompt` (string, optional): Optional prompt to modify the test case generation
- `selectedUserStories` (array, optional): Array of selected user story IDs

**Example:**
```json
{
  "projectUuid": "project-123",
  "suiteUuid": "suite-123",
  "extraPrompt": "Generate comprehensive test coverage",
  "selectedUserStories": ["story-1", "story-2"]
}
```

### 7. wopee_get_app_context

Get existing app context for a project and suite.

**Parameters:**
- `projectUuid` (string, required): UUID of the project
- `suiteUuid` (string, required): UUID of the test suite

**Example:**
```json
{
  "projectUuid": "project-123",
  "suiteUuid": "suite-123"
}
```

### 8. wopee_get_user_stories

Get existing user stories for a project and suite.

**Parameters:**
- `projectUuid` (string, required): UUID of the project
- `suiteUuid` (string, required): UUID of the test suite

**Example:**
```json
{
  "projectUuid": "project-123",
  "suiteUuid": "suite-123"
}
```

### 9. wopee_get_test_cases

Get existing test cases for a project and suite.

**Parameters:**
- `projectUuid` (string, required): UUID of the project
- `suiteUuid` (string, required): UUID of the test suite

**Example:**
```json
{
  "projectUuid": "project-123",
  "suiteUuid": "suite-123"
}
```

### 10. wopee_fetch_analysis_suites

Fetch all analysis suites for a given project.

**Parameters:**
- `projectUuid` (string, required): UUID of the project

**Example:**
```json
{
  "projectUuid": "project-123"
}
```

**Response:**
Returns an array of analysis suites with detailed information including:
- Suite UUID, name, and type
- Upload and execution status
- Analysis identifier
- Suite running status
- Generation state for app context, user stories, and test cases
- Creation and update timestamps

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

- **Command not found**: `npm install -g wopee-mcp`
- **API key error**: Check environment variables
- **Connection failed**: Verify internet and API key
- **Tools not showing**: Restart editor

### Error Handling

#### Common Error Messages

1. **"User not found" error:**
    - Check API key configuration
    - Verify project permissions
    - Contact support if persistent

2. **"Analysis not found" error:**
    - Verify project UUID
    - Check analysis completion status
    - Ensure analysis exists

3. **"Test execution failed" error:**
    - Check test case validity
    - Verify application accessibility
    - Review test steps

### Getting Help

- **Check logs**: Look in the MCP server output panel
- **Verify installation**: Run `wopee-mcp --help` in terminal
- **Test connection**: Use the `wopee_dispatch_analysis` tool with a simple URL

## Response Format

All tools return responses in the following format:

```json
{
  "success": true,
  "data": { /* tool-specific data */ },
  "message": "Success message",
  "error": "Error message (only present if success is false)"
}
```

## Error Handling

The server provides detailed error messages for:
- Invalid parameters
- GraphQL API errors
- Network connectivity issues
- Configuration problems

!!! note "Need help?"

    For support and further information, please refer to the [npm package page](https://www.npmjs.com/package/wopee-mcp) or contact the package maintainers.

*Note: This package is currently in early preview; features and functionalities are subject to change.*

