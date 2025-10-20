# 🔌 HTTP Request Tool

Blend UI and API testing in one seamless flow with the new HTTP Request Tool. Trigger API calls directly within your web tests without context switching or additional setup.

## Overview

The HTTP Request Tool allows you to perform API calls as part of your web testing workflow. This enables you to:

- **Test API endpoints** within the same test flow as UI interactions
- **Validate data** fetched from APIs before or after UI actions
- **Set up test data** via API calls before UI testing begins
- **Verify backend state** after UI operations complete

## What this page covers

How to use HTTP requests in your tests, supported HTTP methods, request/response handling, and best practices for combining API and UI testing.

---

## Supported HTTP methods

The HTTP Request Tool supports all standard HTTP methods:

- **GET** – Retrieve data from an endpoint
- **POST** – Send data to create new resources
- **PUT** – Update existing resources
- **PATCH** – Partial updates to resources
- **DELETE** – Remove resources
- **HEAD** – Get headers without response body
- **OPTIONS** – Get allowed methods for a resource

---

## Making HTTP requests

### Basic syntax

Use the HTTP Request Tool with natural language instructions:

```prompt
Make GET request to https://petstore.swagger.io/v2/pet/123
```

```prompt
Send POST request to https://petstore.swagger.io/v2/pet with body {"name": "Fluffy", "status": "available"}
```

### JSON Configuration

The HTTP Request Tool uses a JSON object to configure requests, following the [RequestInit interface](https://developer.mozilla.org/en-US/docs/Web/API/RequestInit) standard. You can specify:

```json
{
  "method": "POST",
  "headers": {
    "Content-Type": "application/json",
    "Authorization": "Bearer YOUR_TOKEN_HERE"
  },
  "body": "{\"name\": \"John Doe\"}"
}
```

### Request configuration options

The tool supports all standard RequestInit properties:

- **Headers**: Content-Type, Authorization, and custom headers
- **Request body**: JSON, form data, and other content types
- **Query parameters**: URL parameters and query strings
- **Authentication**: Bearer tokens, API keys, and basic auth
- **Cache control**: Cache behavior and policies
- **Credentials**: Cookie and authentication handling
- **Redirect handling**: Follow, error, or manual redirect behavior

---

## Common use cases

### Data validation

Verify API responses before or after UI interactions:

```prompt
Test pet information flow:
- Make GET request to https://petstore.swagger.io/v2/pet/123
- Verify response status is 200
- Navigate to pet details page
- Verify displayed data matches API response
```

### Test data setup

Create test data via API before UI testing:

```prompt
Set up test scenario:
- Send POST request to https://petstore.swagger.io/v2/pet
- Verify pet created successfully
- Navigate to application
- Test pet search with created pet data
```

### Backend verification

Confirm backend state after UI operations:

```prompt
Test pet order placement:
- Navigate to pet store checkout page
- Fill order form and submit
- Make GET request to https://petstore.swagger.io/v2/store/order/latest
- Verify order status is "placed"
```

---

## Request and response handling

### JSON Configuration Examples

The HTTP Request Tool supports comprehensive JSON configuration following the RequestInit standard:

#### Basic POST request
```json
{
  "method": "POST",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "{\"name\": \"Fluffy\", \"status\": \"available\"}"
}
```

#### Request with authentication
```json
{
  "method": "GET",
  "headers": {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

#### Request with custom headers and cache control
```json
{
  "method": "GET",
  "headers": {
    "X-Custom-Header": "custom-value",
    "Accept": "application/json"
  },
  "cache": "no-cache",
  "credentials": "include"
}
```

### Request body formats

The HTTP Request Tool supports multiple content types:

**JSON payloads:**
```prompt
Send POST request to https://petstore.swagger.io/v2/store/order with JSON body:
{
  "petId": 123,
  "quantity": 2,
  "shipDate": "2024-01-15T10:30:00Z",
  "status": "placed"
}
```

**Form data:**
```prompt
Send POST request to https://petstore.swagger.io/v2/user with form data:
username=testuser
firstName=John
lastName=Doe
email=john@example.com
```

### RequestInit Properties

The tool supports all standard RequestInit properties:

- **method**: HTTP method (GET, POST, PUT, DELETE, etc.)
- **headers**: Request headers object
- **body**: Request body (string, FormData, Blob, etc.)
- **cache**: Cache behavior (`default`, `no-store`, `reload`, `no-cache`, `force-cache`)
- **credentials**: Credential handling (`omit`, `same-origin`, `include`)
- **mode**: Request mode (`cors`, `no-cors`, `same-origin`, `navigate`)
- **redirect**: Redirect handling (`follow`, `error`, `manual`)
- **referrer**: Referrer URL
- **referrerPolicy**: Referrer policy
- **integrity**: Subresource integrity hash
- **keepalive**: Keep request alive after page unload
- **signal**: AbortSignal for request cancellation

### Response validation

Validate API responses using assertions:

```prompt
Make GET request to https://petstore.swagger.io/v2/pet/123
- Verify response status is 200
- Verify response contains field "name"
- Verify response field "status" matches "available" or "sold"
```

### Error handling

Test error scenarios and edge cases:

```prompt
Test API error handling:
- Make GET request to https://petstore.swagger.io/v2/pet/999999
- Verify response status is 404
- Verify response contains error message
```

---

## Authentication

### API keys

```json
{
  "method": "GET",
  "headers": {
    "api_key": "special-key"
  }
}
```

### Bearer tokens

```json
{
  "method": "GET",
  "headers": {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
}
```

### Custom headers

```json
{
  "method": "GET",
  "headers": {
    "Authorization": "Bearer your-token-here",
    "X-Custom-Header": "custom-value",
    "Accept": "application/json"
  }
}
```

### Credential handling

```json
{
  "method": "GET",
  "credentials": "include",
  "headers": {
    "Content-Type": "application/json"
  }
}
```

---

## Best practices

!!! tip "HTTP Request Tool best practices"

    - **Test realistic scenarios**: Use API calls that mirror real user workflows
    - **Validate responses**: Always verify API response status and content
    - **Handle authentication**: Include proper authentication for protected endpoints
    - **Test error cases**: Verify API behavior for invalid requests and edge cases
    - **Combine with UI testing**: Use API calls to set up data or verify backend state
    - **Use meaningful assertions**: Verify specific response fields and values
    - **Test different HTTP methods**: Cover GET, POST, PUT, DELETE operations as needed

### Advanced RequestInit Options

#### Cache control
```json
{
  "method": "GET",
  "cache": "no-cache",
  "headers": {
    "Cache-Control": "no-cache"
  }
}
```

#### Request timeout and abort
```json
{
  "method": "POST",
  "body": "{\"data\": \"example\"}",
  "headers": {
    "Content-Type": "application/json"
  },
  "keepalive": true
}
```

#### Cross-origin requests
```json
{
  "method": "GET",
  "mode": "cors",
  "credentials": "include",
  "headers": {
    "Accept": "application/json"
  }
}
```

### When to use HTTP requests

**Good use cases:**
- Setting up test data before UI testing
- Verifying backend state after UI operations
- Testing API endpoints as part of end-to-end flows
- Validating data consistency between UI and API

**Avoid when:**
- Pure UI testing is sufficient
- API testing can be done separately
- You need complex API testing scenarios (use dedicated API testing tools)

---

## Example workflows

### E-commerce order flow

```prompt
Test complete pet order workflow:
1. Make POST request to https://petstore.swagger.io/v2/user
2. Navigate to pet store page
3. Add pet to cart
4. Make GET request to verify cart contents
5. Proceed to checkout
6. Complete purchase
7. Make GET request to verify order status
```

### User authentication flow

```prompt
Test user login with API verification:
1. Send POST request to https://petstore.swagger.io/v2/user/login with credentials
2. Verify response contains valid session
3. Navigate to user profile page
4. Verify user is logged in
5. Make GET request to verify user session
```

### Data synchronization test

```prompt
Test UI-API data sync:
1. Navigate to pet store settings page
2. Update pet information
3. Make GET request to verify changes saved
4. Navigate to pet details page
5. Verify displayed data matches API response
```

---

## Troubleshooting

### Common issues

**Request fails:**
- Verify URL is correct and accessible
- Check authentication credentials
- Ensure proper headers are set
- Verify network connectivity

**Response validation fails:**
- Check response format and structure
- Verify field names and data types
- Ensure response contains expected data
- Review API documentation for correct response format

**Authentication errors:**
- Verify API key or token is valid
- Check token expiration
- Ensure proper authentication header format
- Verify user has required permissions

!!! note "Need help?"

    If you encounter issues with HTTP requests, contact our support team at [help@🦒.io](mailto:help@wopee.io) or visit our [community discussions](https://github.com/orgs/Wopee-io/discussions).

---

## Related topics

- [Tools & Assertions](../concepts/tools-and-assertions.md)
- [Getting Started with Wopee.io Agent testing](../ai-agent.md)
- [Project Context](project-context.md)
- [Analysis Process](../concepts/analysis-process.md)
