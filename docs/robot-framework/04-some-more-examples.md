---
title: Some more examples
---

## Comparison details from response

In order to get comparison details from the response, you can to use any of Wopee.io comparison keywords(`Track`, `Track Fullpage`, or `Track Viewport`).
keyword. This keyword returns a dictionary with keys: `image_url` and `status`.

Example of usage:

```robotframework
*** Test Cases ***
Get comparison details from visual test
    Open Browser ${URL} ${BROWSER}

    &{payload}    Create Dictionary  step_name=${TEST NAME}

    ${result}  Track Fullpage    payload=&{payload}

    Log To Console \n Link to comparison: ${result.image_url}
    Log To Console \n Status of comparison: ${result.status}
```

## More parameters for tracking

You can use more parameters to track during visual testing. Here is an example of usage:

```robotframework
*** Test Cases ***
Visual test with more parameters
    Open Browser ${URL} ${BROWSER}

    &{payload}    Create Dictionary
    ...  step_name=${TEST NAME}
    ...  pixel_to_pixel_diff_tolerance=1
    ...  comment=Hello, world!
    ...  custom_tags=tag1,tag2
    ...  device=desktop
    ...  os=Windows
    ...  browser=Chrome
    ...  viewport=1920x1080

    Track Fullpage    payload=&{payload}
```

## Visual testing for mobile applications

When you test mobile applications for instance with Appium it is possible to use our agnostic approach.
In this case, you need to transform your picture to the base64 format and use the `Track` keyword to compare it.

```robotframework
*** Test Cases ***
Visual test for mobile application
    Open Application    http://localhost:4723/wd/hub
    ...     alias=Myapp1
    ...     platformName=iOS
    ...     platformVersion=7.0
    ...     deviceName='iPhone Simulator'
    ...     app=your.app

    ${image_path}  Capture Page Screenshot
    ${image_base64}    Convert Image to Base64    ${image_path}

    &{payload}    Create Dictionary
    ...  image_base64=${image_base64}
    ...  step_name=${TEST NAME}

    Track    payload=&{payload}

*** Keywords ***
Convert Image to Base64
    [Arguments]    ${image_path}
    ${image_base64}    Evaluate
    ...    sys.modules['base64'].b64encode(open(r"${image_path}", 'rb').read()).decode('utf-8')
    ...    base64
    RETURN    ${image_base64}

```

## Visual testing for pdf documents

When you test pdf documents, you can use our agnostic approach. Convert your pdf to the base64 format and use the `Track` keyword to compare it.

```robotframework
*** Test Cases ***
Visual test for pdf document
    ${pdf_path}  Get File    ${CURDIR}/path/to/your.pdf
    ${pdf_base64}    Convert File To Base64    ${pdf_path}

    &{payload}    Create Dictionary
    ...  image_base64=${pdf_base64}
    ...  step_name=${TEST NAME}

    Track    payload=&{payload}

*** Keywords ***
Convert File To Base64
    [Arguments]    ${file_path}
    ${file_base64}    Evaluate
    ...    sys.modules['base64'].b64encode(open(r"${file_path}", 'rb').read()).decode('utf-8')
    ...    base64
    RETURN    ${file_base64}
```

!!! tip "Robot Framework Visual Regression Testing with Wopee.io"

    Power up your Robot Framework tests with Wopee.io's advanced visual regression testing integration.

    Identify and track visual changes in your web app easily, ensuring consistency across updates. With a quick 1-minute setup, enhance your regression testing and automate visual validations efficiently.

    Try Wopee.io for Robot Framework – [Free Trial](https://cmd.wopee.io), and elevate your visual regression capabilities.

    [Get Started with Wopee.io](https://cmd.wopee.io)
