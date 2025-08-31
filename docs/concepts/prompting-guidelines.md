# Prompting Guidelines - Good Practices

Master the art of writing effective prompts for Wopee.io to generate high-quality tests and documentation.

## Core Prompt Structure

### Basic Template

```markdown
Goal: [What you want to achieve]
Scope: [What to include/exclude]
Assumptions: [What can be assumed]
Constraints: [What to avoid or limit]
Output: [Expected deliverables]
```

### Advanced Template

```markdown
Goal: [Specific objective]
Context: [Background information]
Scope: [Boundaries and limitations]
Assumptions: [Pre-conditions and known state]
Constraints: [Restrictions and exclusions]
Requirements: [Specific needs]
Output: [Expected format and content]
Examples: [Sample outputs if helpful]
```

## High-Signal Prompt Patterns

### Pattern 1: Use browser local storage to store state of the application

```markdown
Goal: Test "Secure Messages" functionality only.
Assumptions: Browser local storage is uploaded and user is authenticated (do not re-login).
Constraints: Do not re-login; focus solely on Secure Messages flows: compose, send, receive, read/unread, attachments.
```

**When to Use**: You have stable modules and want to focus on new features.

### Pattern 2: Apply Page Object Model Structure

```markdown
Goal: Generate tests for "E-commerce Checkout" flow
Context: Swag Labs e-commerce application with login, products, cart, and checkout pages

POM Structure Required:

- BasePage: Common functionality and Wopee integration
- LoginPage: Authentication with methods like login(username, password)
- ProductsPage: Product browsing with methods like addToCart(productName)
- CartPage: Cart management with methods like proceedToCheckout()
- CheckoutPage: Checkout process with methods like fillCheckoutInfo(firstName, lastName, postalCode)
- NavigationPage: Menu and social links handling
```

**When to Use**: You need a complete POM implementation for a multi-page application flow. Wopee.io generates test scenarios and user stories, while you implement the POM structure to ensure optimal maintainability and reusability. This approach gives you full control over your test architecture and allows you to establish consistent patterns across your test suite. Once implemented, these POMs become reusable components that can be referenced in future prompts for generating tests for new features.

### Pattern 3: Constrain Analysis Scope

```markdown
Goal: Test "User Profile" section
Scope: /profile/\* pages only
Assumptions: User is authenticated and can access profile
**Exclude:** Login, navigation, other sections
Focus: Profile editing, avatar upload, preferences
Output: Focused test suite for profile functionality
```

**When to Use**: You want to limit analysis to specific application sections.

### Pattern 4: Generate from Jira and Figma (typically on the 4th step of analysis process)

```markdown
Goal: Generate tests for following user story:

- Title: User can send secure messages
- Description: As a user, I want to send secure messages to other users so that I can communicate privately.

Acceptance Criteria:

- User can compose a new message
- User can select recipients from contact list
- User can attach files up to 10MB
- User can mark message as urgent
- User receives confirmation when message is sent
- User can view sent message in outbox

Technical Notes:

- Messages are encrypted end-to-end
- File upload supports: PDF, DOC, JPG, PNG
- Maximum 5 recipients per message

Assumptions: User is authenticated, UI matches Figma design

Constraints: prefer `data-testid` selectors and use visual click when possible.
```

**When to Use**: You have requirements and designs to incorporate.

### Pattern 5: Focus on Specific Flows

```markdown
Goal: Test "File Upload" feature in messages
Scope: File upload functionality within /messages/compose
Assumptions: User can access message composition
Exclude: Message sending, recipient selection, other features
```

**When to Use**: You want to test specific functionality in detail.

### Pattern 6: Error Handling Focus

```markdown
Goal: Test error scenarios in "User Profile" section
Scope: /profile/\* pages with error conditions
Assumptions: User is authenticated and can access profile
Focus: Validation errors, network failures, permission denied
Exclude: Happy path scenarios (already covered)
Output: Negative test cases and error handling tests
```

**When to Use**: You want to test error conditions and edge cases.

## Do's and Don'ts

### ✅ Do

| Practice                  | Example                                      | Why It Works                            |
| ------------------------- | -------------------------------------------- | --------------------------------------- |
| **Be specific**           | "Test Secure Messages compose functionality" | Clear scope prevents scope creep        |
| **Reference modules**     | "Use existing Login module"                  | Avoids re-analysis of stable components |
| **Set boundaries**        | "Focus on /profile/\* pages only"            | Limits analysis to target areas         |
| **State assumptions**     | "User is authenticated"                      | Provides context for test generation    |
| **Specify output format** | "Generate POM-compatible Playwright tests"   | Ensures desired code structure          |
| **Include constraints**   | "Do not test login flow"                     | Prevents unwanted analysis              |
| **Use examples**          | "Like the LoginPage.ts pattern"              | Provides clear reference                |

### ❌ Don't

| Practice                       | Example                                    | Why It Fails                               |
| ------------------------------ | ------------------------------------------ | ------------------------------------------ |
| **Be vague**                   | "Test the application"                     | Too broad, unclear scope                   |
| **Ignore existing work**       | "Analyze everything"                       | Wastes time re-analyzing stable components |
| **Skip context**               | "Generate tests"                           | Missing assumptions leads to poor results  |
| **Forget constraints**         | "Test all features"                        | May include unwanted functionality         |
| **Unclear output**             | "Create some tests"                        | Unclear format and expectations            |
| **Contradictory instructions** | "Test login but don't test authentication" | Confusing requirements                     |

## Scenario-Specific Templates

### Template 1: E-commerce POM Implementation

Could be used as a initial prompt for new analysis process or to generate tests for specific user story.

```markdown
Goal: Implement complete Page Object Model for "Swag Labs" e-commerce application
Context: Multi-page e-commerce flow with login, products, cart, and checkout

POM Structure Required:

- BasePage: Common functionality, Wopee integration, navigation helpers
- LoginPage: Authentication with business-focused methods
- ProductsPage: Product browsing and cart operations
- CartPage: Cart management and checkout initiation
- CheckoutPage: Checkout process and form handling
- NavigationPage: Menu and social link interactions

Page Object Requirements:

- Extend BasePage for common functionality
- Business-focused method names (e.g., "addBackpackToCart()")
- Private selectors with data-testid attributes
- Visual assertions and Wopee tracking
- Single responsibility principle
- Comprehensive error handling

Example Method Signatures:

- LoginPage: login(username, password), verifyLoginFormFields()
- ProductsPage: addBackpackToCart(), verifyProductsGrid(), goToCart()
- CartPage: proceedToCheckout(), removeBackpackFromCart()
- CheckoutPage: fillCheckoutInfo(firstName, lastName, postalCode), finishOrder()
- NavigationPage: openHamburgerMenu(), clickTwitterLink()
```

### Template 2: New Feature Testing

Could be used as a initial prompt for new analysis process or to generate tests for specific user story.

```markdown
Goal: Test new "Advanced Search" feature
Context: Search functionality with filters, sorting, and pagination
Scope: /search/\* pages and search-related components

Assumptions:

- User is authenticated
- Search index is populated with test data
- Basic search functionality exists

Constraints:

- Do not test basic search (already covered)
- Focus on advanced features only
- Do not modify existing search tests

Requirements:

- Test filter combinations
- Test sorting options
- Test pagination
- Test search result accuracy
```

## When to Apply POM Patterns

### POM Application Guidelines

| Scenario                      | Apply POM | Reason                                  |
| ----------------------------- | --------- | --------------------------------------- |
| **Multi-page applications**   | ✅ Yes    | Complex navigation and state management |
| **E-commerce flows**          | ✅ Yes    | Multiple pages with business logic      |
| **Single page components**    | ❌ No     | Overkill for simple components          |
| **API testing only**          | ❌ No     | No UI interactions needed               |
| **Visual regression testing** | ✅ Yes    | Page-level visual assertions            |
| **End-to-end workflows**      | ✅ Yes    | Complex user journeys                   |

### POM Structure Indicators

**Apply POM when you have:**

- Multiple pages with distinct functionality
- Complex user workflows spanning multiple pages
- Business logic that needs to be encapsulated
- Visual testing requirements
- Need for reusable page interactions
- Team collaboration on test maintenance

**Skip POM when you have:**

- Single page applications with simple interactions
- API-only testing requirements
- Quick exploratory testing
- Simple component testing

## Prompt Optimization Tips

| Tip                         | Poor Example         | Better Example                                                           | Why It Works                            |
| --------------------------- | -------------------- | ------------------------------------------------------------------------ | --------------------------------------- |
| **Start with Clear Goals**  | "Test the app"       | "Test user registration flow with validation scenarios"                  | Specific objectives prevent scope creep |
| **Provide Context**         | "Generate tests"     | "Generate tests for a e-commerce application with user authentication"   | Application context improves relevance  |
| **Set Clear Boundaries**    | "Test everything"    | "Test only the checkout process, exclude product browsing"               | Defined scope focuses analysis          |
| **Reference Existing Work** | "Create login tests" | "Use existing LoginPage.ts module, focus on new authentication features" | Avoids re-analyzing stable components   |
| **Specify Output Format**   | "Create some tests"  | "Generate POM-compatible Playwright tests with TypeScript"               | Ensures desired code structure          |

## Common Mistakes to Avoid

| Mistake                       | Problem Example                        | Solution                                             | Why It Matters                                         |
| ----------------------------- | -------------------------------------- | ---------------------------------------------------- | ------------------------------------------------------ |
| **Overly Broad Scope**        | "Test the entire application"          | Break down into specific features or modules         | Prevents analysis paralysis and unclear results        |
| **Ignoring Existing Modules** | "Generate all tests from scratch"      | Reference existing stable modules                    | Saves time and maintains consistency                   |
| **Unclear Requirements**      | "Test the search feature"              | Specify what aspects of search to test               | Ensures relevant and focused test generation           |
| **Missing Context**           | "Create tests for the form"            | Provide application context and user scenarios       | Improves test relevance and coverage                   |
| **Unrealistic Expectations**  | "Generate perfect tests in one prompt" | Use iterative approach with multiple focused prompts | Achieves better results through incremental refinement |

## Prompt Validation Checklist

Before sending a prompt, verify:

- [ ] **Goal is specific and clear**
- [ ] **Scope is well-defined**
- [ ] **Assumptions are stated**
- [ ] **Constraints are specified**
- [ ] **Output format is clear**
- [ ] **Context is provided**
- [ ] **Existing work is referenced**
- [ ] **Requirements are realistic**

### POM-Specific Validation

When applying POM patterns, also verify:

- [ ] **Page objects are clearly defined** with distinct responsibilities
- [ ] **Business-focused method names** are specified (not technical actions)
- [ ] **BasePage inheritance** is mentioned for common functionality
- [ ] **Visual testing integration** is included if needed
- [ ] **Selector strategy** is specified (data-testid preferred)
- [ ] **Error handling** requirements are outlined
- [ ] **Example usage** demonstrates page object interaction
- [ ] **Single responsibility** principle is maintained
