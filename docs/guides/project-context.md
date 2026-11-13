---
title: Project context
description: "Write a Wopee.io project context that steers the test generator and the AI agent, with a paste-ready template and a filled example."
type: How-to
updated: 13 November 2026
---

# Project context

The project context is one Markdown text per project. It tells Wopee.io how your app works and how to test it. Every generator reads it: the generators of the application description, the user flows, the scenarios and their steps. The AI agent also receives it on every run and crawl. It is available on all plans.

!!! info "For product owners and CTOs"

    Think of the project context as the briefing you would give a new tester on their first day: what the app is, which accounts to use, the business rules, what must never be touched and what counts as a failure. Write it once, and the generator and the agent receive it every time.

## Where to paste it

1. Open the project and go to **More** › **Settings** › **General**. If you pinned **Settings** to the top bar, use that instead. From an analysis, you can also open **Variables & Knowledge** and click **Project context**.
2. Click into the **Project context** field.
3. **Click Switch to markdown before you paste.** See the warning below.
4. Paste the text and click **Save**. If you close the dialog first, Commander asks whether to save your changes.
5. Reopen the field and check the result. Headings must start with `#` and have no backslash in front (`\#`). If they have one, delete the text, switch to markdown and paste again.

!!! warning "Switch to markdown first"

    The field opens as rich text. If you paste there, headings and lists are saved as plain paragraphs and stop working. Click **Switch to markdown** before you paste. If the label reads **Switch to rich text**, you are already in markdown.

Runs and generations that start after you save use the new text.

The text is stored as `data/project-context.md` on the default branch of the project's repository, so one context applies to every analysis. Editing that file in the repository changes the same context.

!!! tip "After you change test data or rules"

    The scenario and step generators take concrete values such as prices, limits and test data from the analysis's **Application description** first, and from the project context only when the description has none. After changing values in the project context, generate the application description again so the old values do not stay.

## Paste-ready template

The template has two parts: a core that every project needs, and optional sections that you paste below it.

1. Copy the core block, then any optional sections you need, into the field. Do not put a code fence around the whole text, because the context is passed to the AI word for word.
2. Replace every `[[...]]` with your own text. Delete a line if it does not apply to your app, for example the cookie-banner line when your app shows no banner, or the sign-out line when tests do not share a signed-in session.
3. Replace the format example under **Writing test descriptions** with one test from your own app. The generator copies its shape.
4. Rename the example variables (`${ADMIN_USERNAME}`, `${ADMIN_PASSWORD}`) to yours. Create every `${NAME}` the text uses as a variable before the first run (see [Variables](../concepts/intent-and-scripted-tests.md#variables)).
5. Before you save, search the pasted text for `[[`. None may remain: anything left goes to the AI word for word on every run.

### Core

````markdown
# Project context

These rules apply to every test the generator writes and every run the agent makes. When a test's own description is more specific, the test wins.

## About the app

- [[One or two lines: what the app does and who uses it.]]
- Main areas, named as they appear on screen: [[Area 1]], [[Area 2]], [[Area 3]].
- Screen language: [[English]]. Numbers: [[1,234.56]]. Dates: [[DD/MM/YYYY]]. Currency: [[GBP]].

## Users and sign-in

- [[Role, e.g. Customer]]: sign in with ${TESTING_USERNAME} and ${TESTING_PASSWORD} using [[the "Sign in" link in the header]].
- [[Second role, e.g. Admin]]: sign in with ${ADMIN_USERNAME} and ${ADMIN_PASSWORD} [[on the admin sign-in page]].
- You are signed in when [[the header shows the account menu]].

## Business rules

- [[How a total or result is calculated, e.g. total = subtotal − discount + shipping.]]
- [[A limit and the message the app shows when it is reached.]]
- [[What a user can save and where it shows afterwards.]]

## Test data

- Each test creates the data it needs and does not depend on another test. Give each new record a unique suffix, such as a timestamp.
- Accounts, passwords and other secrets come from variables written as ${NAME}. Never write a secret into a test.
- Use valid formats for [[country]]: postal code [[format]], phone [[format]]. Never "test" or "123".
- If a test needs a value that is not on the page, in this context or in a variable, stop and report what is missing.

## How to judge a test

- Judge each test only by its own expected results: its PASSES WHEN and MUST NOT lines, or the expected results in its description or steps. If you notice another problem on the way, report it as an issue, but do not fail the test for it.
- A pass needs a value checked on the screen. Check durable results (a saved record, its status, its row in a list), not a toast or an e-mail.
- For values that change on every run (order numbers, dates), check that they are present or contain a fixed part.
- Missing test data or an unreachable environment is reported as such, not as a defect in the app.
- Report each mismatch with the expected value, the shown value and the page where it appears.

## Always and never

- Always accept the cookie banner first ("[[Accept all]]"), before anything else.
- Never send e-mails, messages or invitations to real people. Use only the addresses in variables.
- Never change or delete records the test did not create.
- Never change the password or e-mail of a shared test account.
- Never sign out, except in a test whose goal is signing out: it ends the session other tests use.
````

### Optional sections

````markdown
## Words used on screen

- "[[On-screen term]]" means [[what it is]].

## Key pages

- [[Page name]]: [[https://app.example.com/path]]

## By design (not a bug)

- [[Behaviour that looks wrong but is intended.]] [[What still works next to it.]]

## Out of scope

- [[Third-party pages, e.g. the payment provider or a chat widget.]]
- [[Areas not under test.]]

## Language

- Write test names, descriptions and reports in [[English]]. Quote on-screen labels exactly as shown.

## Writing test descriptions

When you write a test's name and description, put everything in the description, with these labels in capitals, each at the start of its own line, in this order: GOAL, PASSES WHEN, MUST NOT, DATA. One behaviour per test. Name buttons, fields and menus only by their visible label. A description contains no clicks, element IDs or CSS selectors.

Format example (not a test to run):

```text
GOAL: [[One real user goal from your app, in one sentence.]]
PASSES WHEN:
- [[One fact the user can see, with its expected value.]]
- [[Another fact and its expected value.]]
MUST NOT:
- [[What makes the test fail even if the goal is reached.]]
DATA: [[Which account and values to use, as ${NAME} variables.]]
```

For every limit the app states, write tests just below it, at it and just above it. For each form, one test per rule with one expected error, checking that the form does not move on. Count tests by distinct outcomes, not by bullets in a spec.

## Stable locators

- [[Element]]: `[[getByTestId('element-id')]]`

## Before you finish a test description, check

- Every PASSES WHEN line names one fact and its expected value.
- Every test has a MUST NOT line.
- No description contains clicks, element IDs or CSS selectors.
- Every value comes from the page, this context or a variable.
````

## A filled example: demo e-shop

The core and most optional sections, filled in for a fictional home-goods shop. All values are made up.

````markdown
# Project context

These rules apply to every test the generator writes and every run the agent makes. When a test's own description is more specific, the test wins.

## About the app

- An online shop for home goods. Customers browse the catalogue, buy with a card and track orders.
- Main areas, named as they appear on screen: Catalogue, Basket, Checkout, My account, My orders.
- Screen language: English. Numbers: 1,234.56. Dates: DD/MM/YYYY. Currency: GBP.

## Users and sign-in

- Customer: sign in with ${TESTING_USERNAME} and ${TESTING_PASSWORD} using the "Sign in" link in the header.
- Shop admin: sign in with ${ADMIN_USERNAME} and ${ADMIN_PASSWORD} on the Admin sign-in page.
- You are signed in when the header shows "My account".

## Business rules

- Prices include VAT.
- Total = product subtotal − discount + shipping.
- Shipping is 4.90 GBP, and free when the product subtotal is 50.00 GBP or more.
- The test promo code in ${PROMO_CODE} gives 10 % off the product subtotal only. Shipping is never discounted.
- A customer can buy at most 10 units of one product per order. Above that the Basket shows "Maximum 10 per order".
- Addresses saved in My account appear as options at Checkout.

## Test data

- Each test creates the data it needs and does not depend on another test. Give each new address or wishlist a unique suffix, such as a timestamp.
- Accounts, passwords, the promo code and the card number come from variables written as ${NAME}. Never write a secret into a test.
- Use valid UK formats: a postal code in the UK format (e.g. AB1 2CD), phone +44 20 7946 0000.
- If a test needs a value that is not on the page, in this context or in a variable, stop and report what is missing.

## How to judge a test

- Judge each test only by its own expected results: its PASSES WHEN and MUST NOT lines, or the expected results in its description or steps. If you notice another problem on the way, report it as an issue, but do not fail the test for it.
- A placed order counts only when it appears in My orders with its order number. The confirmation e-mail does not count.
- Order numbers and dates change on every run: check that they are present, not their exact text.
- Report each mismatch with the expected value, the shown value and the page where it appears.

## Always and never

- Always accept the cookie banner first ("Accept all"), before anything else.
- Never use the "Contact us" form or the newsletter sign-up with a real address.
- Never change or delete orders, addresses or products the test did not create.
- Never change the password or e-mail of a shared test account.
- Never sign out, except in a test whose goal is signing out.
- Pay only with the test card in ${TEST_CARD_NUMBER}.

## Words used on screen

- "Basket" means the shopping cart.
- "Wishlist" means products saved for later; it is not an order.

## Key pages

- Catalogue: https://shop.example.com/
- Sign in: https://shop.example.com/account/sign-in
- Admin sign-in: https://shop.example.com/admin

## By design (not a bug)

- Products marked "Out of stock" cannot be added to the Basket, but their page opens and "Add to wishlist" works like for any other product.

## Out of scope

- The payment provider's own pages beyond entering the test card.
- The blog and the chat widget.

## Language

- Write test names, descriptions and reports in English. Quote on-screen labels exactly as shown.

## Writing test descriptions

When you write a test's name and description, put everything in the description, with these labels in capitals, each at the start of its own line, in this order: GOAL, PASSES WHEN, MUST NOT, DATA. One behaviour per test. Name buttons, fields and menus only by their visible label. A description contains no clicks, element IDs or CSS selectors.

Format example (not a test to run):

```text
GOAL: A signed-in customer reaches free shipping exactly at the threshold.
PASSES WHEN:
- With a product subtotal just below 50.00 GBP, the Basket shows shipping 4.90 GBP.
- After adding a product that brings the subtotal to 50.00 GBP or more, shipping shows 0.00 GBP.
- The total equals subtotal + shipping, to the penny.
MUST NOT:
- A promo code is used.
DATA: Sign in with ${TESTING_USERNAME}.
```

For every limit the app states, write tests just below it, at it and just above it. For each form, one test per rule with one expected error, checking that the form does not move on. Count tests by distinct outcomes, not by bullets in a spec.

## Stable locators

- Add to basket button: `getByTestId('add-to-basket')`
- Basket item count: `[data-test="basket-count"]`

## Before you finish a test description, check

- Every PASSES WHEN line names one fact and its expected value.
- Every test has a MUST NOT line.
- No description contains clicks, element IDs or CSS selectors.
- Every value comes from the page, this context or a variable.
````

## What each section does

| Section | What it changes |
| --- | --- |
| **About the app** | Shapes the generated application description and tells the agent the formats it will read. |
| **Users and sign-in** | How to sign in for each role. Whether a test signs in belongs in the test; how to sign in belongs here. |
| **Business rules** | Gives the generator values to compute expectations from, and gives the agent rules to check against. |
| **Test data** | Prevents collisions between tests and invented values. |
| **How to judge a test** | Sets what a pass needs. The first rule stops a general rule here from failing a test that checked what it was asked to. |
| **Always and never** | Safety limits for every run. |
| **Words used on screen** | The generator and the agent use your terms instead of guessing. |
| **Key pages** | A generated step may open a URL directly only in three cases: it is the starting URL, it was seen during the crawl, or it is written out here or in the analysis instructions. Other URLs are turned into steps through the UI. Write each URL in full (`https://...`) or as a path (`/account/sign-in`). The match is on host and path, so `/sign-in-help` does not cover `/sign-in`. |
| **By design** | Stops false alarms. Say exactly what still works, or the agent may skip a real defect next to it. |
| **Out of scope** | Keeps generation and crawls away from areas you do not test. |
| **Language** | The language of generated tests and reports, and how to quote labels. |
| **Writing test descriptions** | Asks the generator to write descriptions in the intent format of [Intent-driven and Scripted Tests](../concepts/intent-and-scripted-tests.md). The generator copies a worked example more reliably than it follows abstract rules. The rules cover descriptions only, because the same context also goes to **Generate steps** and to steps saved from a run. Check the first scenarios generated after you add this section. If they do not follow the format, also add it to **Additional instructions** in **Generate scenarios**. This section shapes how tests are written. It does not stop steps from being saved: switch **Save steps from this run** off, or run the tests from a Test Plan. |
| **Stable locators** | Generated steps may use a CSS selector or test ID only when it is written word for word here. When there are no screenshots to support a locator, the generator drops every locator that does not appear exactly in the project context. Write locators exactly as a step would use them, in backticks. |
| **Before you finish** | A short self-check at the end of the context. Models tend to follow a final checklist, but nothing enforces it. |

## Do and don't

| Do | Don't |
| --- | --- |
| Write rules: "Shipping is free from 50.00 GBP" | Write steps: "Click Basket, then click Checkout" |
| Say when a test fails: MUST NOT lines, a fail rule per test | Leave failure to the agent's judgement |
| Use `${TESTING_USERNAME}`, `${TESTING_PASSWORD}` and your own variables | Paste passwords, tokens or real card numbers |
| Name roles and how each signs in | Explain how to sign in "if needed" in every test |
| Write out a value the agent must judge by eye | Expect `${NAME}` to be filled in inside a visual check or the agent's reasoning; it is filled in only when the agent types, selects, opens a URL or checks text with a text assertion |
| Use obvious placeholders in examples | Use realistic sample values; they can show up in reports as if they were read from the page |
| Say each rule once | Repeat or contradict a rule; with two versions, the AI may follow either one |
| Put a check that only one test needs into that test | Put a pass or fail rule for one test into the context; it applies to every test |
| Use triggers the agent can see: a message, a value, its own actions | Use elapsed time ("after 5 minutes") or page source; the agent knows the date and time when the run starts, but not how much time has passed |
| Name exact on-screen labels in quotes | Describe elements vaguely ("the blue button") |
| Keep it short and current | List past incidents, run IDs, dates or issue numbers |
| Write calm, factual rules | Write commands such as "ignore", "override" or "bypass"; this wording can trip the AI model's content filter and fail the run |

## Size

The field has no character limit, but the whole text goes to the AI with every generation and every step of every run. A longer context makes generation and runs slower and more expensive, and rules in the middle of a long text are followed less reliably. Aim for one to two screens of text: the core sections and only the optional sections you need. Put app details that belong to one analysis into that analysis instead.

## Project context, application description and instructions

| What | Where | Scope |
| --- | --- | --- |
| Shared rules, roles, test data rules, never-do rules, description format | **Project context** | Every analysis, every generation, every run |
| What the app shows: features, values, prices on screen | **Application description** (Variables & Knowledge) | One analysis; every generation, and sent to the agent as application context on every run |
| Background for one analysis, such as how to sign in or navigate | The analysis's **Instructions** (next to **Project URL** in the analysis inputs) | One analysis; sent to the agent on every run as supplementary background, used only when the test needs it |
| A focus for one generation, e.g. "add coverage for checkout with an expired card" | **Additional instructions** in **Generate scenarios** | One analysis; saved and sent with every generation in it, not to runs |
| Know-how the agent applies during runs | **Skills** (Variables & Knowledge) | See [Self-Healing](../concepts/self-healing.md) |
| A check that must hold for one test | The test's **Description** | One test |

## Change it with the Assistant

You can ask the **Assistant** to change the project context. It proposes the change as a **Change to project context** card with **Apply**, **Edit** and **Discard**. Only a project admin can apply it.

## Troubleshooting

### The context is not applied

- Check that you clicked **Save** in Project Settings.
- Reopen the field. If headings show a backslash (`\#`), the text was pasted as rich text: paste it again after **Switch to markdown**.
- Runs that were already running keep the old text; start a new run.
- New values do not appear in generated tests: generate the application description again (see the tip under [Where to paste it](#where-to-paste-it)).

### A rule is not followed

- Make it a list item with one rule, and say why if the reason is not obvious.
- Look for a second rule that contradicts it, in the context, the test or the analysis instructions.
- If the rule must hold for one test, write it into that test's description: a test's own words take priority.

## Related topics

- [Intent-driven and Scripted Tests](../concepts/intent-and-scripted-tests.md)
- [Prompting Guidelines](../concepts/prompting-guidelines.md)
- [Verdict Integrity](../concepts/verdict-integrity.md)
- [Self-Healing](../concepts/self-healing.md)
- [Tools & Assertions](../concepts/tools-and-assertions.md)
- [Getting Started with Wopee.io Agent testing](../ai-agent.md)

!!! note "Need help?"

    For project context questions, contact our support team at [help@wopee.io](mailto:help@wopee.io) or visit our [community discussions](https://github.com/orgs/Wopee-io/discussions).
