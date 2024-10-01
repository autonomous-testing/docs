---
title: Overview
---

## Getting started

There are several ways to initiate visual testing with Wopee.io and Robot Framework. It can be used with the Browser library, Selenium library, or for any picture comparison (e.g., PDF, mobile or desktop apps).

You can use all of the options in two ways:

1. Library: By adding tracking keywords into your test cases
2. Listener: Without modifying your test and automatically collecting visual validation

To quickly explore most of the options, you can start with the Robot Framework Integration Template Project.

The listener approach is simpler to set up, while the library approach offers more customization. Choose the method that best suits your project requirements and preferences.

<div class="grid cards" markdown>

- [Getting Started >> ](/integrations/robot-framework/02-manual-setup)

</div>

## Wopee.io + Robot Framework

Wopee.io seamlessly integrates with Robot Framework to improve test coverage, speed up maintenance, and ensure more robust test runs. With a vision of autonomous visual testing, Wopee.io facilitates easy integration of visual validation into your existing Robot Framework tests, adding an extra layer of quality assurance. With Wopee.io, you can easily compare screenshots (from web and mobile testing), compare various images (including PDFs, desktop apps, or test data images captured or processed by your application under test), manage baselines, and automate visual testing within your Robot Framework test suite.

Robot Framework is a versatile open-source automation framework for acceptance testing, acceptance test-driven development (ATDD), and robotic process automation (RPA). It features an easy-to-use tabular test data syntax and follows a keyword-driven testing approach. The testing capabilities of Robot Framework can be extended by test libraries implemented either with Python or Java. Furthermore, users can create new higher-level keywords from existing ones using the same syntax used for creating test cases.

Robot Framework offers the following key features:

- **Simple and readable syntax:** It has an easy-to-understand tabular syntax for writing test cases.
- **Keyword-Driven testing:** Tests can be organized into reusable keywords for efficient test creation and maintenance.
- **Cross-Platform support:** It allows tests to be run on different operating systems and browsers.
- **Extensive library support:** Users can utilize a wide range of libraries for various functionalities.
- **Built-in reporting:** It can generate detailed reports for test execution results.
- **Flexible test data handling:** It enables efficient management of test data using tabular syntax and variables.
- **Integration with other tools:** It can be integrated with other tools and frameworks to enhance testing capabilities.

---

## The benefits of integrating Robot Framework with Wopee.io

**Basic features:**

- **Image comparison**: Accurately compare screenshots to detect visual differences, providing more thorough validation than Robot Framework's assertions alone.
- **Ignore areas**: Specify areas to ignore during comparisons by locator or coordinates, reducing false positives.
- **Baseline management**: Efficiently handle baselines with bulk approval, filtering options, and the ability to flexibly tag baselines for better organization and control.

**Advanced features:**

- **Baseline version history**: Track changes over time with detailed version histories.
- **Multi-branch and multi-config support**: Easily manage tests across different branches and configurations.
- **Improved team collaboration**: Enhance teamwork with features designed for better collaboration and communication.
- **Archiving**: Keep your workspace organized with archiving capabilities for old or irrelevant tests.

Our implementation of Robot Framework with Wopee.io enables testing of web applications (using Selenium or Playwright) and mobile applications (using Appium). Additionally, it supports testing various other applications, including PDFs, desktop apps, and custom images generated or processed by your application. This integration offers a robust visual validation solution that enhances the testing capabilities of Robot Framework. It ensures more resilient test executions, faster maintenance, and higher quality web applications.

Furthermore, users can **benefit from Wopee.io's visual testing bot**, which automates and streamlines the visual testing process, ensuring thorough and consistent validation without manual intervention.

Integrating Robot Framework with Wopee.io offers significant benefits for modern web application testing. Robot Framework provides a flexible, keyword-driven testing approach with easy-to-understand syntax, while Wopee.io enhances this by adding robust visual validation capabilities. This integration allows for advanced baseline management, enabling efficient handling of baselines with features like bulk approval, filtering, and flexible tagging. It also improves team collaboration with enhanced tools and supports comprehensive visual testing with automated comparison algorithms. Overall, combining Robot Framework with Wopee.io ensures more resilient test runs, faster maintenance, and higher quality web applications.

!!! tip "Robot Framework Visual Regression Testing with Wopee.io"

    Power up your Robot Framework tests with Wopee.io's advanced visual regression testing integration.

    Identify and track visual changes in your web app easily, ensuring consistency across updates. With a quick 1-minute setup, enhance your regression testing and automate visual validations efficiently.

    Try Wopee.io for Robot Framework – [Free Trial](https://cmd.wopee.io), and elevate your visual regression capabilities.

    [Get Started with Wopee.io](https://cmd.wopee.io)
