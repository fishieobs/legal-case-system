(function () {
  var active = (document.currentScript && document.currentScript.getAttribute("data-active")) || "";
  var pages = [
    { id: "cases",     href: "index.html",      label: "⚖ 案件系統" },
    { id: "clients",   href: "clients.html",     label: "👥 客戶管理" },
    { id: "judgments", href: "judgments.html",   label: "🔨 判決書管理" },
    { id: "letters",   href: "letters.html",     label: "📮 信函管理" },
    { id: "documents", href: "documents.html",   label: "📁 文件管理" },
    { id: "templates", href: "templates.html",   label: "📚 文書範本" },
    { id: "tax",       href: "tax.html",         label: "💰 稅務管理" },
    { id: "court",     href: "court_nav.html",   label: "🗺 開庭助理" },
    { id: "widget",    href: "widget.html",      label: "📅 庭期 Widget" },
    { id: "deadline",  href: "deadline.html",    label: "⏱ 時效計算器" },
    { id: "checklist",      href: "checklist.html",      label: "📋 開庭清單" },
    { id: "judicial-search",href: "judicial-search.html",label: "🔍 裁判書查詢" },
    { id: "fees",           href: "fees.html",           label: "💰 律師費計算" },
  ];

  // ── Global theme (dark / light), shared across all pages ──
  // Legacy per-page keys are kept in sync so pages with their own
  // theme logic (index, letters, judgments, court_nav) stay consistent.
  var THEME_KEYS = ["appTheme", "themeMode", "lettersTheme", "jTheme", "navTheme"];

  function readTheme() {
    try {
      var t = localStorage.getItem("appTheme");
      if (!t) {
        for (var i = 1; i < THEME_KEYS.length; i++) {
          var v = localStorage.getItem(THEME_KEYS[i]);
          if (v) { t = v; break; }
        }
      }
      return t || "dark";
    } catch (e) { return "dark"; }
  }

  function effectiveTheme(t) {
    if (t === "auto") {
      var h = new Date().getHours();
      return (h >= 6 && h < 20) ? "light" : "dark";
    }
    return t === "light" ? "light" : "dark";
  }

  function applyTheme(t) {
    document.documentElement.classList.toggle("light", effectiveTheme(t) === "light");
  }

  function setTheme(t) {
    try { THEME_KEYS.forEach(function (k) { localStorage.setItem(k, t); }); } catch (e) {}
    applyTheme(t);
    updateThemeBtn();
  }

  function updateThemeBtn() {
    var btn = document.getElementById("sys-nav-theme");
    if (!btn) return;
    var isLight = document.documentElement.classList.contains("light");
    btn.textContent = isLight ? "🌙" : "☀️";
    btn.title = isLight ? "切換深色模式" : "切換淺色模式";
  }

  applyTheme(readTheme());

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
      ".sys-nav-logo{font-size:14px;color:rgba(200,169,110,.5);margin-right:6px;flex-shrink:0;border-right:1px solid rgba(200,169,110,.2);padding-right:10px;}" +
      ".sys-nav-theme{margin-left:auto;flex-shrink:0;background:transparent;border:1px solid rgba(200,169,110,.25);border-radius:7px;padding:4px 10px;font-size:13px;cursor:pointer;line-height:1;transition:all .15s;}" +
      ".sys-nav-theme:hover{border-color:rgba(200,169,110,.6);background:rgba(200,169,110,.08);}" +
      ":root.light .sys-nav{background:rgba(255,255,255,.96);border-bottom-color:rgba(138,92,26,.25);}" +
      ":root.light .sys-nav-item.active{background:rgba(138,92,26,.1);color:#8a5c1a;border-color:rgba(138,92,26,.3);}" +
      ":root.light a.sys-nav-item{color:#6b7280;}" +
      ":root.light a.sys-nav-item:hover{background:rgba(138,92,26,.06);color:#8a5c1a;border-color:rgba(138,92,26,.2);}" +
      ":root.light .sys-nav-logo{color:rgba(138,92,26,.5);border-right-color:rgba(138,92,26,.2);}" +
      ":root.light .sys-nav-theme{border-color:rgba(138,92,26,.25);}" +
      ":root.light .sys-nav-theme:hover{border-color:rgba(138,92,26,.6);background:rgba(138,92,26,.06);}";
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
  html += '<button class="sys-nav-theme" id="sys-nav-theme" type="button" aria-label="切換深淺色模式">☀️</button>';
  nav.innerHTML = html;

  var body = document.body;
  if (body.firstChild) body.insertBefore(nav, body.firstChild);
  else body.appendChild(nav);

  updateThemeBtn();
  document.getElementById("sys-nav-theme").addEventListener("click", function () {
    var isLight = document.documentElement.classList.contains("light");
    setTheme(isLight ? "dark" : "light");
  });
})();
