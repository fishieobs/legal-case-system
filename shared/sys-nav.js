(function () {
  var active = (document.currentScript && document.currentScript.getAttribute("data-active")) || "";
  var pages = [
    { id: "cases",     href: "index.html",      label: "⚖ 案件系統" },
    { id: "judgments", href: "judgments.html",   label: "🔨 判決書管理" },
    { id: "letters",   href: "letters.html",     label: "📮 信函管理" },
    { id: "templates", href: "templates.html",   label: "📚 文書範本" },
    { id: "tax",       href: "tax.html",         label: "💰 稅務管理" },
    { id: "court",     href: "court_nav.html",   label: "🗺 開庭助理" },
    { id: "widget",    href: "widget.html",      label: "📅 庭期 Widget" },
    { id: "deadline",  href: "deadline.html",    label: "⏱ 時效計算器" },
    { id: "checklist",      href: "checklist.html",      label: "📋 開庭清單" },
    { id: "judicial-search",href: "judicial-search.html",label: "🔍 裁判書查詢" },
  ];

  if (!document.getElementById("sys-nav-css")) {
    var style = document.createElement("style");
    style.id = "sys-nav-css";
    style.textContent =
      ".sys-nav{position:fixed;top:0;left:0;right:0;z-index:9999;background:rgba(5,10,24,.96);backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);border-bottom:1px solid rgba(200,169,110,.25);display:flex;align-items:center;gap:2px;padding:6px 12px;overflow-x:auto;scrollbar-width:none;}" +
      ".sys-nav::-webkit-scrollbar{display:none;}" +
      ".sys-nav-item{display:inline-flex;align-items:center;padding:6px 14px;border-radius:7px;font-size:12px;font-weight:700;white-space:nowrap;font-family:'Noto Sans TC',sans-serif;transition:all .15s;text-decoration:none;border:1px solid transparent;}" +
      ".sys-nav-item.active{background:rgba(200,169,110,.15);color:#c8a96e;border-color:rgba(200,169,110,.3);cursor:default;}" +
      "a.sys-nav-item{color:#64748b;}" +
      "a.sys-nav-item:hover{background:rgba(200,169,110,.08);color:#c8a96e;border-color:rgba(200,169,110,.2);}" +
      ".sys-nav-logo{font-size:14px;color:rgba(200,169,110,.5);margin-right:6px;flex-shrink:0;border-right:1px solid rgba(200,169,110,.2);padding-right:10px;}";
    document.head.appendChild(style);
  }

  var nav = document.createElement("div");
  nav.className = "sys-nav";
  nav.setAttribute("role", "navigation");
  nav.setAttribute("aria-label", "系統導覽");

  var html = '<span class="sys-nav-logo">⚖</span>';
  for (var i = 0; i < pages.length; i++) {
    var p = pages[i];
    if (p.id === active) {
      html += '<span class="sys-nav-item active">' + p.label + "</span>";
    } else {
      html += '<a class="sys-nav-item" href="' + p.href + '">' + p.label + "</a>";
    }
  }
  nav.innerHTML = html;

  var body = document.body;
  if (body.firstChild) body.insertBefore(nav, body.firstChild);
  else body.appendChild(nav);
})();
