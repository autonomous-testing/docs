// Code blocks, tables and tab bars that scroll sideways can be scrolled with the keyboard
(function () {
  function mark() {
    document.querySelectorAll(".md-code__content, .md-typeset__scrollwrap, .tabbed-labels").forEach(function (el) {
      if (el.scrollWidth > el.clientWidth + 1) el.tabIndex = 0;
      else if (el.getAttribute("tabindex") === "0") el.removeAttribute("tabindex");
    });
  }
  if (typeof document$ !== "undefined") document$.subscribe(mark);
  else document.addEventListener("DOMContentLoaded", mark);
  var t;
  function later() {
    clearTimeout(t);
    t = setTimeout(mark, 200);
  }
  window.addEventListener("resize", later);
  document.addEventListener("change", later);
  if (document.fonts) document.fonts.ready.then(later);
})();
