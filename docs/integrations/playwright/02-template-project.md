---
title: Template Project
---

This is an ideal starting point for visual testing with Wopee.io and Playwright. Our template project includes a pre-configured setup for visual testing using Playwright and Wopee.io. Additionally, we provide a demo test that you can execute to see it in action.

## Prerequisites

- [Node.js](https://nodejs.org/en/download/)
- Visual Studio Code or any other code editor
- Playwright project set up (if you don't have one, follow the [Playwright Getting Started](https://playwright.dev/docs/intro){: target="\_blank"} guide)
- Wopee.io [free account](https://cmd.wopee.io){: target="\_blank"}

## Create a new Playwright project

1. Navigate to Wopee.io [project page](https://cmd.wopee.io/projects) and click `New Integration` button `Playwright`.
   ![New project button](/img/new-project.png)

2. Fill in the project name, url and click `Create`.
   ![New project form](/img/new-project-form.png)

## Environment setup (API key, project UUID)

??? tip "Where to find project UUID and Wopee.io API key?"

    You can find your project UUID and Wopee.io API key in the project settings screen after navigating to project.

    ![Project UUID](/img/project-settings.gif)

### Set Wopee.io API key

Before running the visual test, set up your API key as an environment variable named `WOPEE_API_KEY`.
You may set it from the command line like this:

=== "Linux/MacOS"

    ```shell
    export WOPEE_API_KEY=your-api-key
    ```

=== "Windows"

    ```shell
    set WOPEE_API_KEY=your-api-key
    ```

### Set `.env` file params

Template repository comes with sample environment file. You can easily reuse it and set your own `.env` file. To do so copy or rename `.env.example` file into `.env`.

All parameters are already set in `.env.example` file. You need to set only `WOPEE_PROJECT_UUID` parameter.

## Get template project

Clone repository using VS Code palette option (Ctrl + Shift + P): `https://github.com/Wopee-io/playwright-template` or by running:

    git clone https://github.com/Wopee-io/playwright-template

## Install dependencies

Install all dependencies:

    npm i

## Run tests

Run first demo test:

    npm t

You can also run tests in Docker container (Docker need to installed on your machine):

    npm run tests-in-docker
