function hideToCForSpecificPages() {
    var currentUrl = window.location.pathname;
  
    // List of pages where the ToC should be hidden
    var pagesWithoutToC = [
      '/',                  // Root homepage (index.md)
      '/index.html'         // Sometimes MkDocs uses /index.html for the homepage
    ];
  
    // Check if current URL is in the list of pages to hide the ToC
    var toc = document.querySelector('.md-nav--secondary');

    if (pagesWithoutToC.includes(currentUrl)) {
      if (toc) {
        toc.style.display = 'none';
      }
    } else {
      if (toc) {
        toc.style.display = '';
      }
    }
  }
  
  // Listen for the initial page load
  document.addEventListener('DOMContentLoaded', function() {
    hideToCForSpecificPages();
  });