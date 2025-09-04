# 🗄️ Browser local storage

Configure and upload browser local storage data to ensure your tests run with the necessary application state and user preferences.

## Overview

Browser local storage is crucial for testing web applications that rely on client-side data persistence. Wopee.io allows you to upload and configure local storage data that will be available during test execution, ensuring tests run with realistic application states.

## What is browser local storage?

Local storage is a web storage mechanism that allows web applications to store data locally within a user's browser. This data includes:

- **User preferences**: Theme settings, language choices, display options
- **Authentication tokens**: Session tokens, API keys, refresh tokens
- **Application state**: Shopping cart contents, form data, user progress
- **Cache data**: Frequently accessed information, user-specific configurations

## How to obtain browser storage data

To capture browser storage data for your tests, you'll use Playwright's built-in test generator (`codegen`) tool. This tool allows you to record your browser interactions and automatically save the resulting storage state.

### Step 1: Install Playwright (if not already installed)

```bash
npm install -D @playwright/test
```

### Step 2: Generate storage state using Playwright codegen

Use the `codegen` command with the `--save-storage` flag to capture browser storage:

```bash
npx playwright codegen --save-storage=auth.json [your-website-url]
```

**Examples:**

```bash
# For a specific website
npx playwright codegen --save-storage=auth.json https://example.com

# For local development
npx playwright codegen --save-storage=auth.json http://localhost:3000

# Without URL (you can navigate manually)
npx playwright codegen --save-storage=auth.json
```

### Step 3: Authenticate and interact with your application

When the browser window opens:

1. **Navigate to your application** (if not already there)
2. **Perform authentication** (login, etc.)
3. **Navigate through pages** you want to test
4. **Interact with features** that set storage data
5. **Stop recording** by closing the browser window or pressing the stop button

### Step 4: Verify the generated file

After closing the browser, verify that `auth.json` was created in your current directory. The file should contain your browser's storage state including cookies, localStorage, sessionStorage, and IndexedDB data.

### Step 5: Move the file to your repository

Move the generated `auth.json` file to your repository's `data` directory:

```bash
mkdir -p data
mv auth.json data/
```

### Complete workflow example

Here's a complete example for capturing authentication state:

```bash
# 1. Start codegen with storage saving
npx playwright codegen --save-storage=auth.json https://myapp.com

# 2. In the browser window that opens:
#    - Navigate to the login page
#    - Enter your credentials
#    - Complete the login process
#    - Navigate to a few key pages
#    - Close the browser

# 3. Move the file to your repository
mkdir -p data
mv auth.json data/

# 4. Verify the file structure
ls -la data/auth.json
```

### Advanced codegen options

You can customize the codegen process with additional options:

```bash
# Emulate specific device
npx playwright codegen --device="iPhone 13" --save-storage=auth.json https://cmd.wopee.io

# Set specific viewport size
npx playwright codegen --viewport-size="1920,1080" --save-storage=auth.json https://cmd.wopee.io

# Emulate dark mode
npx playwright codegen --color-scheme=dark --save-storage=auth.json https://cmd.wopee.io

# Use existing browser profile (for persistent authentication)
npx playwright codegen --user-data-dir=/path/to/browser/profile --save-storage=auth.json https://cmd.wopee.io
```

### Testing the captured storage state

Before using the file in your tests, verify it works correctly:

```bash
# Test the captured authentication state
npx playwright codegen --load-storage=auth.json https://myapp.com
```

If the storage state is correct, you should see your application in an authenticated state when the browser opens.

### Troubleshooting storage capture

**Common issues and solutions:**

- **No file generated**: Ensure you close the browser window properly or stop recording
- **Empty file**: Make sure you actually perform actions that set storage data
- **Missing data**: Navigate through more pages and interact with features that use storage
- **Authentication not captured**: Complete the full login flow before stopping recording

**File size considerations:**

- Consider cleaning up unnecessary storage entries
- Focus on essential authentication and state data

## Supported storage types

Wopee.io AI Agent automatically loads data from the `data` directory. It is based on Playwright's [browser context](https://playwright.dev/docs/test-state#browser-context) and supports multiple browser storage mechanisms:

### localStorage

Key-value pairs stored persistently in the browser.

### sessionStorage

Temporary storage that lasts for the duration of the page session.

### Cookies

Small pieces of data stored by the browser for specific domains.

### IndexedDB

More complex database storage for larger amounts of structured data.

## How to upload local storage data: JSON Context File

Upload a complete browser context file to your repository's `data` directory. The AI testing agent will automatically detect and apply this storage state.

Create a file named `auth.json` in your `data` directory (example):

```json
{
  "cookies": [
    {
      "name": "session-username",
      "value": "standard_user",
      "domain": "www.saucedemo.com",
      "path": "/",
      "expires": 1752609084,
      "httpOnly": false,
      "secure": false,
      "sameSite": "Lax"
    }
  ],
  "origins": [
    {
      "origin": "https://www.saucedemo.com",
      "localStorage": [
        {
          "name": "backtrace-guid",
          "value": "b6ff9051-63fb-49f5-9ce9-7706db9c4960"
        },
        {
          "name": "backtrace-last-active",
          "value": "1752608467035"
        }
      ]
    }
  ]
}
```

## File organization in your repository

### Repository structure

Place your browser context files in the `data` directory of your repository:

```
your-repository/
├── data/
│   └── auth.json          # Authentication context
├── tests/
└── src/
```

### Naming conventions

- Use file name: `auth.json`
- The agent automatically loads the the JSON file

## Storage data formats

### Origin-based localStorage format

The recommended format organizes storage by domain origin:

```json
{
  "origins": [
    {
      "origin": "https://cmd.wopee.io",
      "localStorage": [
        {
          "name": "user_id",
          "value": "12345"
        },
        {
          "name": "settings",
          "value": "{\"theme\": \"dark\", \"notifications\": true}"
        }
      ]
    }
  ]
}
```

### Cookies configuration

Cookies are specified in an array with detailed properties:

```json
{
  "cookies": [
    {
      "name": "auth_session", // Cookie name
      "value": "encrypted_session_data", // Cookie value
      "domain": ".cmd.wopee.io", // Domain scope
      "path": "/", // Path scope
      "expires": 1752609084, // Unix timestamp
      "secure": true, // HTTPS only
      "httpOnly": false, // JavaScript accessible
      "sameSite": "Lax" // SameSite policy
    }
  ]
}
```

### IndexedDB data

Complex structured data for IndexedDB:

```javascript
{
  "databases": [
    {
      "name": "MyAppDB",
      "version": 1,
      "stores": [
        {
          "name": "users",
          "data": [
            {"id": 1, "name": "John Doe", "email": "john@example.com"},
            {"id": 2, "name": "Jane Smith", "email": "jane@example.com"}
          ]
        }
      ]
    }
  ]
}
```

## Using storage data in tests

### Automatic detection and application

When you commit a JSON context file to your repository's `data` directory:

1. **Automatic detection**: The AI agent scans the `data` directory for JSON files during test initialization
2. **Context loading**: When found, the agent logs "Browser storage state found and to be uploaded"
3. **Browser initialization**: A new browser context is created with the pre-configured storage state
4. **State persistence**: All cookies, localStorage, and sessionStorage remain available throughout the test session
5. **Cross-domain support**: Storage data is applied per origin, supporting multi-domain applications

This seamless integration means tests automatically start with your configured authentication, user preferences, and application state.

### Practical example: Setting up authentication

1. **Create the context file**: Add `auth.json` to your `data` directory:

```json
{
  "cookies": [
    {
      "name": "session-username",
      "value": "standard_user",
      "domain": "www.saucedemo.com",
      "path": "/",
      "expires": 1752609084,
      "httpOnly": false,
      "secure": false,
      "sameSite": "Lax"
    }
  ],
  "origins": [
    {
      "origin": "https://www.saucedemo.com",
      "localStorage": [
        {
          "name": "user-session",
          "value": "authenticated"
        },
        {
          "name": "user-role",
          "value": "standard"
        }
      ]
    }
  ]
}
```

2. **Run your tests**: The AI agent will automatically detect this file and initialize the browser with this authentication state

3. **Tests start authenticated**: Your tests begin as if the user is already logged in, skipping login steps

## Common use cases

### Authentication testing

Pre-configure authentication tokens and user sessions:

```json
{
  "localStorage": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "refresh_token": "def456ghi789jkl012mno345pqr678stu901",
    "user_profile": "{\"id\": 123, \"role\": \"admin\", \"permissions\": [\"read\", \"write\"]}"
  },
  "cookies": [
    {
      "name": "session_id",
      "value": "secure_session_hash",
      "domain": ".myapp.com",
      "secure": true,
      "httpOnly": true
    }
  ]
}
```

### E-commerce testing

Set up shopping cart and user preferences:

```json
{
  "localStorage": {
    "shopping_cart": "{\"items\": [{\"product_id\": 456, \"quantity\": 2, \"price\": 29.99}], \"total\": 59.98}",
    "user_preferences": "{\"currency\": \"USD\", \"shipping_address\": \"123 Main St\"}",
    "recently_viewed": "[456, 789, 123, 654]",
    "wishlist": "[789, 321, 555]"
  }
}
```

### Application state testing

Configure complex application states:

```json
{
  "localStorage": {
    "app_state": "{\"current_page\": \"dashboard\", \"sidebar_collapsed\": false}",
    "user_settings": "{\"theme\": \"dark\", \"language\": \"en\", \"timezone\": \"UTC\"}",
    "feature_flags": "{\"beta_ui\": true, \"advanced_features\": false}",
    "cache_timestamp": "2024-01-15T10:30:00Z"
  },
  "sessionStorage": {
    "form_data": "{\"step\": 3, \"completed_steps\": [1, 2]}",
    "temp_calculations": "{\"total\": 1250.50, \"tax\": 125.05}"
  }
}
```

## Best practices

!!! tip "Local storage best practices"

    - **Data consistency**: Ensure storage data matches your application's expected format
    - **Token validity**: Use valid, non-expired authentication tokens
    - **Minimal data**: Include only necessary data to avoid bloating
    - **Security**: Avoid real user credentials in test storage data
    - **Versioning**: Maintain different storage configurations for different test scenarios

## Environment-specific configurations

### Development environment

```json
{
  "localStorage": {
    "api_endpoint": "https://dev-api.myapp.com",
    "debug_mode": "true",
    "log_level": "debug"
  }
}
```

### Staging environment

```json
{
  "localStorage": {
    "api_endpoint": "https://staging-api.myapp.com",
    "debug_mode": "false",
    "log_level": "info"
  }
}
```

### Production-like testing

```json
{
  "localStorage": {
    "api_endpoint": "https://api.myapp.com",
    "debug_mode": "false",
    "log_level": "error"
  }
}
```

## Troubleshooting

### Storage not applied

- Verify JSON format is valid
- Check that domain settings match your application
- Ensure storage keys match application expectations

### Authentication issues

- Validate token format and expiration
- Check cookie domain and path settings
- Verify authentication flow compatibility

### Data format errors

- Ensure nested JSON is properly escaped
- Validate data types match application requirements
- Check for special characters in values

### Performance issues

- Reduce storage data size if tests are slow
- Avoid large IndexedDB datasets
- Clean up unnecessary storage entries

!!! warning "Security considerations"

    - Never use real user credentials in test storage data
    - Avoid storing sensitive information in plain text
    - Use test-specific tokens and session data
    - Regularly rotate test authentication data

!!! note "Need help?"

    For browser storage configuration issues, contact our support team at [help@wopee.io](mailto:help@wopee.io) or visit our [community discussions](https://github.com/orgs/Wopee-io/discussions).
