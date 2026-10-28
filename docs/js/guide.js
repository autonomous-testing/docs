(function () {
  var stop = ".wo-pager, .md-source-file, .md-feedback, .md-tags";
  function scrollables(article) {
    article.querySelectorAll(".md-typeset__scrollwrap").forEach(function (wrap) {
      if (wrap.scrollWidth > wrap.clientWidth) wrap.tabIndex = 0;
    });
  }
  function enhance() {
    var meta = document.querySelector(".wo-page-meta");
    if (!meta) return;
    var article = meta.parentNode;
    if (!meta.hasAttribute("data-wo-steps") || article.querySelector(".wo-step")) return scrollables(article);
    var heads = Array.prototype.filter.call(article.children, function (el) {
      return el.tagName === "H2" && /^\d+\.\s/.test(el.textContent);
    });
    heads.forEach(function (h) {
      var section = document.createElement("section");
      section.className = "wo-step";
      h.parentNode.insertBefore(section, h);
      var el = h;
      while (el && !(el !== h && (el.tagName === "H2" || el.matches(stop)))) {
        var next = el.nextElementSibling;
        section.appendChild(el);
        el = next;
      }
      var text = h.firstChild;
      var m = text && text.nodeType === 3 && text.data.match(/^(\d+)\.\s+/);
      if (m) {
        text.data = text.data.slice(m[0].length);
        var n = document.createElement("span");
        n.className = "wo-step__n";
        n.textContent = m[1];
        h.insertBefore(n, text);
      }
      if (!section.nextElementSibling || !section.nextElementSibling.classList.contains("wo-step")) {
        section.classList.add("wo-step--last");
      }
    });
    scrollables(article);
  }
  if (typeof document$ !== "undefined") document$.subscribe(enhance);
  else document.addEventListener("DOMContentLoaded", enhance);
})();
