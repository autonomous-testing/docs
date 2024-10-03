---
title: Template project
---

The following steps will guide you through the setup of the template project. If you want a faster alternative, you can use the [Makefile](/robot-framework/03-setup-with-make) to automate the setup process. However, following the instructions below will give you a better understanding of the project structure.

## Prerequisites

- [Python](https://www.python.org/downloads/) >=3.11
- [Node.js](https://nodejs.org/en/download/) - in case you want to run Browser library tests
- Visual Studio Code or any other code editor
- Wopee.io [account](https://cmd.wopee.io)

## Environment setup

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

??? tip "Where to find project UUID and Wopee.io API key?"

    You can find your project UUID and Wopee.io API key in the project settings screen after navigating to project.

    ![Project UUID](/img/project-settings.gif)

## Get template project

Clone repository using VS Code palette option (Ctrl + Shift + P): `https://github.com/Wopee-io/robotframework-template` or by running:

    git clone https://github.com/Wopee-io/robotframework-template

!!! tip

    You can save your time by using Makefile to automate the setup process and run tests easier. Check out our [Set up with Makefile](/robot-framework/03-setup-with-make) documentation for more details.

## Create and activate virtual environment

This step is optional but recommended:

```shell
python -m venv .venv
source .venv/bin/activate
```

## Install dependencies

Install all dependencies:

    pip install -r requirements.txt

!!! note

    We are using GitHub repository to store our python package. Make sure your `requirements.txt` file refer to the latest version of the package.
    You can find our Robot Framework releases [here](https://github.com/Wopee-io/robotframework-template/releases/).

!!! note

    If you want to run Browser library tests you need to install additional dependencies:

    ```shell
    rfbrowser init
    ```

## Run tests

To run it with Wopee.io library approach, execute the following command:

### Run for any picture comparison

```shell
robot tests/selenium_agnostic.robot
```

### Run with Selenium library

```shell
export WOPEE_DRIVER_LIBRARY=SeleniumLibrary && \
robot tests/selenium_standalone.robot
```

### Run with Browser library

```shell
export WOPEE_DRIVER_LIBRARY=BrowserLibrary && \
robot tests/browser_standalone.robot
```

To run it with Wopee.io listener approach, execute the following command:

### Running listener with Selenium library

```shell
export WOPEE_DRIVER_LIBRARY=SeleniumLibrary && \
robot --listener 'wopee_rf.Listener:--dot_env_path:.env' tests/selenium_listener.robot
```

### Running listener with Browser library

```shell
export WOPEE_DRIVER_LIBRARY=BrowserLibrary && \
robot --listener 'wopee_rf.Listener:--dot_env_path:.env' tests/browser_listener.robot
```

!!! note

    When you are using only one of the libraries, you can set `WOPEE_DRIVER_LIBRARY` in your `.env` file however make sure you are not overwriting.
    Following commands might be also handy:

    ```shell
    echo $WOPEE_DRIVER_LIBRARY # make sure it is not set otherwise it will overwrite your settings from .env file
    unset WOPEE_DRIVER_LIBRARY # you can unset it if you want to use settings from .env file
    ```
