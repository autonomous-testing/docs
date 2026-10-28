---
title: Some more examples
description: Wopee.io visual testing examples for Robot Framework. Read the comparison result, pass extra parameters, track the viewport, and compare mobile app screenshots and PDF pages.
---

# Examples

The examples assume the setup from [Getting started](01-getting-started.md): `wopee_rf` installed and a `.env` with `WOPEE_SCREENSHOT_VALIDATION_ENABLED=true` and `WOPEE_DRIVER_LIBRARY`. Every Wopee.io keyword takes named arguments only.

## Comparison details from the result

`Track`, `Track Fullpage` and `Track Viewport` return the result of the comparison: `step_name`, `status` and `image_url`, the link to the step in Commander.

```robotframework
*** Settings ***
Library     Browser
Library     wopee_rf.Standalone    dot_env_path=.env

Test Teardown    Stop Scenario

*** Test Cases ***
Get comparison details
    New Page          https://www.saucedemo.com
    Start Scenario    scenario_name=${TEST NAME}    suite_name=Examples

    ${result}=    Track Fullpage    step_name=Login page

    Log To Console    \nStatus: ${result.status}
    Log To Console    Link to comparison: ${result.image_url}
    Should Not Be Equal    ${result.status}    unresolved
```

`status` is `new`, `ok`, `unresolved` or `autoApproved`. The last line fails the test on a difference for this one step. To do that for every step, set `WOPEE_ENABLE_SOFT_ASSERT=false` instead (see [Fail the test on a visual difference](02-manual-setup.md#fail-the-test-on-a-visual-difference)).

## More parameters for tracking

The optional parameters are stored with the screenshot and shown in Commander. They override the matching `WOPEE_*` environment variable for this step.

```robotframework
*** Test Cases ***
Visual test with more parameters
    New Page          https://www.saucedemo.com
    Start Scenario    scenario_name=${TEST NAME}    suite_name=Examples

    Track Fullpage
    ...    step_name=Login page
    ...    pixel_to_pixel_diff_tolerance=1
    ...    comment=Hello, world!
    ...    custom_tags=tag1,tag2
    ...    device=desktop
    ...    os=Windows
    ...    browser=Chrome
    ...    viewport=1920x1080
```

`pixel_to_pixel_diff_tolerance` is the difference in percent that still counts as a match.

## Viewport or full page

`Track Fullpage` scrolls through the page and captures all of it. `Track Viewport` captures only what is visible, which is faster and ignores content below the fold.

```robotframework
*** Test Cases ***
Header only
    New Page             https://www.saucedemo.com
    Set Viewport Size    1280    720
    Start Scenario       scenario_name=${TEST NAME}    suite_name=Examples

    Track Viewport    step_name=Above the fold
```

Keep the viewport size the same between runs. A different size produces a different screenshot and an `unresolved` step.

## Several tests in one run

The library starts fresh in every test case, so pass the suite name in each test. Tests with the same suite name end up in the same run:

```robotframework
*** Variables ***
${SUITE}    Shop ${{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}}

*** Test Cases ***
Login page
    New Page          https://www.saucedemo.com
    Start Scenario    scenario_name=Login       suite_name=${SUITE}
    Track Fullpage    step_name=Login page

Products page
    New Page          https://www.saucedemo.com
    Fill Text         id=user-name    standard_user
    Fill Text         id=password     secret_sauce
    Click             id=login-button
    Start Scenario    scenario_name=Products    suite_name=${SUITE}
    Track Fullpage    step_name=Products
```

## Visual testing for mobile applications

For Appium, or any other tool that saves a screenshot as a file, read the PNG, encode it to base64 and pass it to `Track`. `Track` needs no driver library, but the `robotframework-browser` package must be installed (see [Configuration and listener › SeleniumLibrary](02-manual-setup.md#seleniumlibrary)).

```robotframework
*** Settings ***
Library     AppiumLibrary
Library     wopee_rf.Standalone    dot_env_path=.env

Test Teardown    Stop Scenario

*** Test Cases ***
Visual test for a mobile application
    Open Application    http://localhost:4723
    ...    platformName=Android
    ...    automationName=UiAutomator2
    ...    app=${CURDIR}/app.apk

    Start Scenario    scenario_name=${TEST NAME}    suite_name=Mobile

    ${path}=    Capture Page Screenshot
    ${image}=    Image To Base64    ${path}
    Track    image_base64=${image}    step_name=Start screen    device=Pixel 8    os=Android 15

*** Keywords ***
Image To Base64
    [Arguments]    ${path}
    ${image}=    Evaluate    base64.b64encode(pathlib.Path(r"${path}").read_bytes()).decode()    modules=base64,pathlib
    RETURN    ${image}
```

## Visual testing for PDF documents

Wopee.io compares images, so render each PDF page to PNG first. This example uses [PyMuPDF](https://pymupdf.readthedocs.io) (`pip install pymupdf`) and tracks every page as its own step:

```robotframework
*** Settings ***
Library     wopee_rf.Standalone    dot_env_path=.env

Test Teardown    Stop Scenario

*** Test Cases ***
Visual test for a PDF document
    Start Scenario    scenario_name=Invoice PDF    suite_name=Documents

    @{pages}=    PDF Pages To Base64    ${CURDIR}/invoice.pdf
    FOR    ${index}    ${page}    IN ENUMERATE    @{pages}    start=1
        Track    image_base64=${page}    step_name=Page ${index}
    END

*** Keywords ***
PDF Pages To Base64
    [Arguments]    ${pdf_path}
    @{pages}=    Evaluate
    ...    [base64.b64encode(p.get_pixmap(dpi=100).tobytes("png")).decode() for p in pymupdf.open(r"${pdf_path}")]
    ...    modules=base64,pymupdf
    RETURN    @{pages}
```

Keep the same `dpi` between runs, because it sets the image size.
