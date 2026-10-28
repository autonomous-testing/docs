document.addEventListener("click", function (event) {
  var link = event.target.closest("a[data-yt]");
  if (!link || event.metaKey || event.ctrlKey || event.shiftKey) return;
  event.preventDefault();
  var frame = document.createElement("iframe");
  frame.src = "https://www.youtube-nocookie.com/embed/" + link.dataset.yt + "?autoplay=1&rel=0";
  frame.title = link.dataset.title || "Video";
  frame.allow = "autoplay; encrypted-media; picture-in-picture; clipboard-write";
  frame.referrerPolicy = "strict-origin-when-cross-origin";
  frame.allowFullscreen = true;
  link.parentNode.replaceChild(frame, link);
  frame.focus();
});

document.addEventListener("DOMContentLoaded", function () {
  var search = document.querySelector(".md-search[role=dialog]");
  if (search && !search.hasAttribute("aria-label")) search.setAttribute("aria-label", "Search");
});
