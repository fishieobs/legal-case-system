(function () {
  var active = (document.currentScript && document.currentScript.getAttribute("data-active")) || "";
  var pages = [
    { id: "cases",     href: "index.html",      label: "⚖ 案件系統" },
    { id: "widget",    href: "widget.html",      label: "📅 庭期 Widget" },
    { id: "clients",   href: "clients.html",     label: "👥 客戶管理" },
    { id: "fees",           href: "fees.html",           label: "💰 律師費計算" },
    { id: "judgments", href: "judgments.html",   label: "🔨 判決書管理" },
    { id: "letters",   href: "letters.html",     label: "📮 信函管理" },
    { id: "documents", href: "documents.html",   label: "📁 文件管理" },
    { id: "templates", href: "templates.html",   label: "📚 文書範本" },
    { id: "tax",       href: "tax.html",         label: "💰 稅務管理" },
    { id: "court",     href: "court_nav.html",   label: "🗺 開庭助理" },
    { id: "deadline",  href: "deadline.html",    label: "⏱ 時效計算器" },
    { id: "checklist",      href: "checklist.html",      label: "📋 開庭清單" },
    { id: "judicial-search",href: "judicial-search.html",label: "🔍 裁判書查詢" },
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
    // legal-design-tw：宣紙暖白底、墨字、朱印紅重點色（單一紙本主題，字面色值以確保
    // 於尚未改版的頁面也能正確顯示，不依賴各頁 CSS 變數）。
    style.textContent =
      ".sys-nav{position:fixed;top:0;left:0;right:0;z-index:9999;background:#FFFFFF;border-bottom:1px solid #C4BAA6;display:flex;align-items:center;gap:2px;padding:6px 12px;overflow-x:auto;scrollbar-width:none;}" +
      ".sys-nav::-webkit-scrollbar{display:none;}" +
      ".sys-nav-item{display:inline-flex;align-items:center;padding:6px 13px;border-radius:2px;font-size:13px;font-weight:700;white-space:nowrap;font-family:'BiauKai','DFKai-SB','標楷體','KaiTi','STKaiti','Kaiti TC','Noto Serif TC',serif;letter-spacing:.03em;transition:all .15s;text-decoration:none;border:1px solid transparent;}" +
      ".sys-nav-item.active{background:#F3E3DF;color:#9E2A24;border-color:#9E2A24;cursor:default;}" +
      "a.sys-nav-item{color:#5B554D;}" +
      "a.sys-nav-item:hover{background:#F3E3DF;color:#9E2A24;border-color:transparent;}" +
      ".sys-nav-logo{font-size:15px;color:#9E2A24;margin-right:6px;flex-shrink:0;border-right:1px solid #DDD5C7;padding-right:10px;}" +
      ".sys-nav-theme{margin-left:auto;flex-shrink:0;background:transparent;border:1px solid #C4BAA6;border-radius:2px;padding:4px 10px;font-size:13px;cursor:pointer;line-height:1;color:#5B554D;transition:all .15s;}" +
      ".sys-nav-theme:hover{border-color:#9E2A24;color:#9E2A24;background:#F3E3DF;}";
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
