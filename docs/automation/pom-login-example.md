# POM: Reusable Login Module

On this example we will create a robust, reusable login module that Wopee.io can reference without re-analysis. This guide shows you how to build, register, and use login components efficiently.

## pages/LoginPage.ts

```typescript
import { Page, Locator, expect } from "@playwright/test";

export class LoginPage {
  readonly page: Page;
  readonly usernameInput: Locator;
  readonly passwordInput: Locator;
  readonly loginButton: Locator;
  readonly errorMessage: Locator;
  readonly forgotPasswordLink: Locator;

  constructor(page: Page) {
    this.page = page;
    this.usernameInput = page.locator('[data-testid="username-input"]');
    this.passwordInput = page.locator('[data-testid="password-input"]');
    this.loginButton = page.locator('[data-testid="login-button"]');
    this.errorMessage = page.locator('[data-testid="error-message"]');
    this.forgotPasswordLink = page.locator('[data-testid="forgot-password"]');
  }

  async goto() {
    await this.page.goto("/login");
    await this.page.waitForLoadState("networkidle");
  }

  async login(username: string, password: string) {
    await this.usernameInput.fill(username);
    await this.passwordInput.fill(password);
    await this.loginButton.click();

    // Wait for navigation or success indicator
    await this.page.waitForURL("**/dashboard", { timeout: 10000 });
  }

  async loginWithInvalidCredentials(username: string, password: string) {
    await this.usernameInput.fill(username);
    await this.passwordInput.fill(password);
    await this.loginButton.click();

    // Wait for error message
    await this.errorMessage.waitFor({ state: "visible" });
  }

  async getErrorMessage() {
    return await this.errorMessage.textContent();
  }

  async isLoggedIn() {
    // Check for dashboard URL or authenticated user indicator
    return (
      this.page.url().includes("/dashboard") ||
      (await this.page.locator('[data-testid="user-menu"]').isVisible())
    );
  }

  async logout() {
    await this.page.locator('[data-testid="user-menu"]').click();
    await this.page.locator('[data-testid="logout-button"]').click();
    await this.page.waitForURL("**/login");
  }
}
```