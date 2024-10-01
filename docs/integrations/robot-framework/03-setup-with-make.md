---
title: Setup with Make
---

This makes some steps easier to run. You can use the Makefile to run tests with a single command.

## Prerequisites

Follow initial steps from the [Manual setup](/integrations/robot-framework/02-manual-setup) to set up your environment.
There is point in the documentation referring back here. Once you have your environment set up, you can proceed with the following steps.

We prepared a Makefile to automate following steps to demonstrate how to run tests with Robot Framework and Wopee.io.

## Installation

Create and activate a virtual environment and install dependencies.

Run: `make install`

This step creates a virtual environment and installs all dependencies.
Also .env file is created with the default values. You have to modify it to set your Wopee.io API key and project UUID.

## Running tests

Execute tests with Robot Framework and Wopee.io.

- Agnostic - Run tests with the any framework or event for the pdf comparison. To do so transform your picture to the base64 format and use the Wopee.io library to compare it. Use `make test` to run the tests.
- Selenium library - Run tests with the Selenium library: `make test.selenium`
- Browser library - Run tests with the Browser library: `make test.browser`
- Listener w. Selenium library - Run tests with the listener approach: `make test.selenium.listener`
- Listener w. Browser library - Run tests with the listener approach: `make test.browser.listener`

## Cleaning

Remove the reports directory: `make clean`
