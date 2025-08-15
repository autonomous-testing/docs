# 🌍 Project context

Configure global instructions and context that guide the AI testing agent's behavior across all tests in your project.

## Overview

Global project context provides a way to give the AI testing agent specific instructions, preferences, and contextual information about your application. These instructions are automatically loaded and applied whenever the Wopee.io AI testing agent executes tests.

## What is global context?

Global project context includes:

- **Testing instructions**: Specific guidance on how tests should be performed
- **Application behavior**: How your application works and what to expect
- **User interaction preferences**: Language, formatting, and interaction style
- **Business rules**: Domain-specific requirements and constraints
- **Testing scenarios**: Common patterns and workflows in your application

## How to set up project context

### Creating the context file

Create a `project-context.md` file in your repository's `data` directory. The AI testing agent will automatically load and apply these instructions during test execution.

```
your-repository/
├── data/
│   ├── project-context.md    # Global instructions for AI agent
│   └── auth.json            # Browser storage context
├── tests/
└── src/
```

### Basic context structure

The `project-context.md` file uses simple markdown format to provide instructions:

```markdown
# Project Context for AI Testing Agent

## Application Information

This is an e-commerce platform for selling organic products.

## Testing Instructions

- All form inputs should be filled in Spanish
- Use emojis extensively in text fields where appropriate
- Always use EUR currency for currency fields

## Application Behavior

- Product search results appear after typing 3+ characters
- Shopping cart updates immediately when items are added
- When user is logged in, there is avatar and user initials in the top left corner of the page
- When user is not logged in, there is login button in the top right corner of the page
- When user is logged in, there is logout button in the top right corner of the page
```

## Real-world context examples

### E-commerce platform

```markdown
# Project Context for AI Testing Agent

## Application Information

This is a luxury fashion e-commerce platform targeting Spanish-speaking customers.

## Testing Instructions

- Always fill forms in Spanish (e.g., "Juan García" for names, "Calle Mayor 123" for addresses)
- Use appropriate Spanish email formats: usuario@ejemplo.es
- Select "España" as country and "EUR" as currency
- Use fashion-related emojis when filling product reviews: ✨👗🛍️💎

## Application Behavior

- Product images take 2-3 seconds to load due to high resolution
- Size charts appear as overlays when clicking "Guía de tallas"
- Free shipping banner shows only for orders over €50
- Guest checkout requires email verification step

## Business Rules

- VIP customers (loyalty tier "Oro") get 24h early access to sales
- Returns are only available for 30 days, except for undergarments
- International shipping is disabled for leather products
```

### Banking application

```markdown
# Project Context for AI Testing Agent

## Application Information

This is a mobile banking app for a German financial institution.

## Testing Instructions

- Use German formatting for amounts: 1.234,56 € (dot for thousands, comma for decimals)
- Fill dates in DD.MM.YYYY format
- Use German addresses: "Hauptstraße 45, 10115 Berlin"
- IBAN validation requires DE country code format

## Application Behavior

- All transactions require 2FA via SMS or authenticator app
- Account balance updates may take 10-15 seconds after transactions
- PDF statements are generated asynchronously - wait for email notification
- Session timeout occurs after 15 minutes of inactivity

## Security Requirements

- Never use real account numbers - use test IBANs starting with DE89370400440532013000
- Sensitive actions trigger additional PIN verification
- Transaction history shows only last 90 days by default
```

### Healthcare platform

```markdown
# Project Context for AI Testing Agent

## Application Information

This is a patient portal for a healthcare provider with HIPAA compliance requirements.

## Testing Instructions

- Use realistic but fake medical data: "Type 2 Diabetes", "Hypertension"
- Patient names should follow format: "LastName, FirstName MiddleInitial"
- Use medical terminology correctly: "Prescription" not "Medicine"
- Always verify privacy notices are displayed before entering sensitive data

## Application Behavior

- Medical history loads in paginated chunks of 10 records
- Prescription refill requests require pharmacy selection
- Appointment scheduling shows availability 2 weeks in advance
- Lab results appear with 24-48 hour delay after tests

## Compliance Requirements

- All test data must be clearly marked as "TEST PATIENT - NOT REAL"
- Screenshots cannot contain any identifiable information
- Session expires after 20 minutes for security
- Audit logs are generated for all data access
```

### Educational platform

```markdown
# Project Context for AI Testing Agent

## Application Information

This is a learning management system for K-12 education with multilingual support.

## Testing Instructions

- Use age-appropriate student names: "Emma Thompson", "Liam Johnson"
- Fill assignment submissions with educational content, not lorem ipsum
- Use encouraging emojis in feedback: 📚✏️⭐🎓
- Select appropriate grade levels: "Grade 3", "Grade 7", etc.

## Application Behavior

- Video lessons buffer for 5-10 seconds before playing
- Quiz auto-saves every 30 seconds
- Grade calculations update overnight (not real-time)
- Parent notifications are sent via email and SMS

## Educational Requirements

- Content must be age-appropriate for selected grade level
- Assignments have due dates that affect late penalty calculations
- Student progress tracking includes time spent on activities
- Accessibility features must work with screen readers
```

## How the AI agent uses project context

### Automatic loading

When you place a `project-context.md` file in your repository's `data` directory, the AI testing agent automatically:

1. **Loads instructions** during test initialization
2. **Applies context** to all testing decisions and actions
3. **Follows preferences** for language, formatting, and interaction style
4. **Respects business rules** and application-specific behavior
5. **Maintains consistency** across all test executions

### Context application examples

If your context specifies "All inputs should be in Spanish", the agent will:

- Fill name fields with "María González" instead of "John Doe"
- Use Spanish addresses: "Calle Principal 123, Madrid"
- Select Spanish language options in dropdowns
- Write Spanish text in comment fields and reviews

### Context-aware testing benefits

With project context in place, your AI testing becomes:

- **Culturally appropriate**: Tests use correct language, formats, and cultural conventions
- **Domain-specific**: Agent understands your business terminology and processes
- **Consistent**: All tests follow the same guidelines and preferences
- **Realistic**: Test data matches your actual user patterns and requirements

## Context organization tips

### Structuring your context file

Organize your `project-context.md` file in clear sections:

```markdown
# Project Context for AI Testing Agent

## Application Information

Brief description of your application and its purpose.

## Testing Instructions

- Specific guidelines for how tests should be performed
- Language and formatting preferences
- Data entry requirements

## Application Behavior

- How your application works and responds
- Timing expectations and loading behaviors
- Special features or interactions

## Business Rules

- Domain-specific requirements
- Validation rules and constraints
- Workflow requirements

## Error Handling

- Expected error messages and how to handle them
- Recovery procedures for failed operations
```

## Best practices

!!! tip "Project context best practices"

    - **Be specific**: Provide clear, actionable instructions rather than vague guidelines
    - **Use examples**: Include concrete examples of preferred data formats and values
    - **Keep updated**: Regularly review and update context as your application evolves
    - **Test your context**: Verify that the AI agent correctly applies your instructions
    - **Version control**: Track context changes alongside your code changes

## Common context patterns

### Language and localization

```markdown
## Testing Instructions

- All form inputs should be in French
- Use French date format: DD/MM/YYYY
- Currency should always be EUR with French formatting: 1 234,56 €
- Use French postal codes: 75001, 69001, etc.
- Select "France" as country in all dropdowns
```

### Industry-specific terminology

```markdown
## Application Behavior

- Medical appointments are called "consultations"
- Use ICD-10 codes for diagnoses: E11.9 for diabetes
- Patient consent forms must be acknowledged before proceeding
- Insurance verification takes 30-45 seconds to process
```

### UI interaction preferences

```markdown
## Testing Instructions

- Use emojis extensively in social media posts: 🎉✨💝🌟
- Fill bio fields with creative, personality-rich content
- Use hashtags in relevant fields: #fashion #style #trendy
- Profile photos should represent diverse demographics
```

## Troubleshooting

### Context not being applied

- Verify `project-context.md` file exists in the `data` directory
- Check markdown syntax is valid
- Ensure file is committed to your repository
- Confirm the AI agent can access the file during test execution

### Instructions not being followed

- Make instructions more specific and actionable
- Add concrete examples of expected behavior
- Check for conflicting instructions within the context
- Test with simpler instructions first, then add complexity

### File organization issues

- Ensure file is named exactly `project-context.md`
- Verify the file is in the correct `data` directory path
- Check file permissions allow reading

!!! warning "Context considerations"

    - Avoid including sensitive information in context files
    - Keep instructions clear and unambiguous
    - Test context changes in a development environment first
    - Remember that context affects all tests in the project

!!! note "Need help?"

    For project context configuration issues, contact our support team at [help@wopee.io](mailto:help@wopee.io) or visit our [community discussions](https://github.com/orgs/Wopee-io/discussions).
