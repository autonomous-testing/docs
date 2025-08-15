# 📥 Download files

Test your web application's file download functionality to ensure users can successfully download files, reports, and other content.

## Overview

File downloads are a common feature in web applications, from document exports to media downloads. Wopee.io helps you test these download functionalities to ensure they work correctly across different browsers and scenarios.

## Types of downloadable files to test

### Common web app downloads

- **Documents**: PDFs, Word documents, spreadsheets, presentations
- **Reports**: Generated reports, analytics exports, user data exports
- **Media files**: Images, videos, audio files, graphics
- **Data exports**: CSV files, JSON exports, database backups
- **Software**: Installers, updates, mobile apps
- **Templates**: Document templates, configuration files

### Dynamic vs static downloads

- **Static files**: Pre-existing files stored on the server
- **Dynamic files**: Generated on-demand based on user data or requests
- **Streaming downloads**: Large files downloaded in chunks
- **Authenticated downloads**: Files requiring login or permissions

## How to test file downloads

### Creating download tests with AI

Use prompts to generate tests that verify download functionality:

!!! tip "Use prompt for download testing"

    Create tests that verify file download functionality with specific prompts.

    ```prompt
    Create test with following steps:

    - Navigate to `https://example.com/reports`
    - Click the "Download PDF Report" button
    - Verify that a PDF file was downloaded
    - Check that the downloaded file is not empty
    ```

### Manual test creation

1. Navigate to your project in [Wopee Commander](https://cmd.wopee.io): Project > Analysis > Test
2. Click "Add new user story" or "Add new test" for existing user story
3. Add steps that include download interactions:
   - Click download buttons or links
   - Verify download completion
   - Check file properties (size, format, content)
4. Save and run the test

### Testing different download scenarios

Create comprehensive tests for various download patterns:

#### Direct download links

```prompt
Test direct file download:
- Navigate to `https://example.com/files`
- Click on "sample-document.pdf" link
- Verify PDF file downloads successfully
- Check file size is greater than 0 bytes
```

#### Form-based downloads

```prompt
Test report generation and download:
- Navigate to `https://example.com/reports`
- Select date range from "2024-01-01" to "2024-01-31"
- Click "Generate Report" button
- Wait for report generation
- Click "Download Report" button
- Verify CSV file downloads with correct data
```

## Download verification methods

### What to verify in download tests

When testing file downloads, verify these aspects:

=== "File Properties"

    ```prompt
    Verify download properties:
    - Check that file was downloaded
    - Verify file size is greater than 0 bytes
    - Confirm correct file extension (.pdf, .csv, .xlsx)
    - Check filename matches expected pattern
    ```

=== "File Content"

    ```prompt
    Verify download content:
    - Open downloaded PDF and check it contains data
    - Verify CSV has correct headers and data rows
    - Check image files display correctly
    - Confirm document formatting is preserved
    ```

=== "Download Timing"

    ```prompt
    Test download performance:
    - Measure time from click to download completion
    - Verify download doesn't timeout
    - Check progress indicators work correctly
    - Test download cancellation functionality
    ```

## AI testing agent for downloads

### Automatic download handling

When using AI testing agent, file downloads are automatically handled:

- **Download detection**: Automatically detects when downloads are triggered
- **File verification**: Checks that files are successfully downloaded
- **Content validation**: Basic verification that files contain data
- **Format checking**: Confirms file extensions match expected types

The AI agent will automatically:

- Click download buttons and links
- Wait for download completion
- Verify downloaded files exist
- Check basic file properties (size, format)
- Report download success or failure

### Advanced download testing

For more complex download scenarios, use specific prompts:

#### Testing authenticated downloads

```prompt
Test secure file download:
- Login with username "testuser" and password "password123"
- Navigate to "My Documents" section
- Click "Download Confidential Report"
- Verify PDF downloads successfully
- Logout and verify download link no longer works
```

#### Testing bulk downloads

```prompt
Test multiple file download:
- Navigate to file gallery
- Select 3 images using checkboxes
- Click "Download Selected" button
- Verify ZIP file downloads containing all 3 images
- Extract ZIP and confirm all files are present
```

#### Testing download permissions

```prompt
Test download access control:
- Login as regular user
- Navigate to admin reports section
- Attempt to download "Admin Only Report"
- Verify access denied message appears
- Login as admin user
- Verify same report downloads successfully
```

## Download test scenarios

### E-commerce downloads

Test digital product delivery and receipts:

```prompt
Test digital product download:
- Add digital product to cart
- Complete purchase process
- Go to "My Downloads" page
- Click download link for purchased item
- Verify digital product file downloads
- Test download limit restrictions
```

### Report generation testing

Test dynamic report creation:

```prompt
Test custom report generation:
- Navigate to analytics dashboard
- Select "Last 30 days" date range
- Choose "Sales Report" type
- Click "Generate Report" button
- Wait for "Report Ready" notification
- Click "Download Report" button
- Verify Excel file downloads with correct data
```

### Media download testing

Test image and video downloads:

```prompt
Test media gallery downloads:
- Navigate to photo gallery
- Click on high-resolution image
- Click "Download Original" button
- Verify high-quality image downloads
- Check file size is larger than thumbnail
- Test download of different image formats
```

## Best practices

!!! tip "Download testing best practices"

    - **Test different file types**: Verify downloads work for PDFs, images, documents, etc.
    - **Check file integrity**: Ensure downloaded files are not corrupted
    - **Test download limits**: Verify restrictions on file size, download attempts, etc.
    - **Browser compatibility**: Test downloads across different browsers
    - **Network conditions**: Test downloads with slow/unstable connections
    - **Authentication**: Verify download permissions and access controls

## Common download patterns to test

### Direct download links

- Static files linked directly from pages
- Right-click "Save As" functionality
- Download progress indicators

### Generated file downloads

- Reports created on-demand
- Export functionality from databases
- Customized documents based on user input

### Authenticated downloads

- Login-protected files
- Role-based download permissions
- Session-dependent file access

### Bulk download operations

- Multiple file selection and download
- ZIP archive creation and download
- Batch export functionality

## Troubleshooting download tests

### Download not working

- Check if download button/link is correctly identified
- Verify the element selector is accurate
- Ensure download triggers are properly clicked
- Check for JavaScript-based download mechanisms

### Download verification fails

- Increase wait time for large file downloads
- Check if download location is accessible
- Verify file naming patterns match expectations
- Ensure browser download settings allow automatic downloads

### Authentication issues

- Verify login credentials are correct
- Check if session hasn't expired during test
- Ensure user has proper permissions for file access
- Test download links work manually first

### Browser-specific issues

- Some browsers block automatic downloads
- Different browsers have different download behaviors
- Test across multiple browser types
- Check browser download directory settings

!!! warning "Testing considerations"

    - Large files may timeout during automated tests
    - Some download types require specific browser configurations
    - Network speed affects download test reliability
    - Browser popup blockers may interfere with downloads

!!! note "Need help?"

    For download testing issues, contact support at [help@wopee.io](mailto:help@wopee.io) or check our [community discussions](https://github.com/orgs/Wopee-io/discussions).
