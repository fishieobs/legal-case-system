(function () {
  var active = (document.currentScript && document.currentScript.getAttribute("data-active")) || "";

  // ══════════════════════════════════════════════════════════
  // 介面配色（主題）— 覆寫各頁共用的 design tokens，一處定義全系統生效
  // ══════════════════════════════════════════════════════════
  var THEMES = [
    { id: "paper", label: "宣紙", dot: "#FAF7F0", ring: "#9E2A24" },
    { id: "ink",   label: "墨金", dot: "#111C2E", ring: "#C9A96A" },
    { id: "night", label: "玄墨", dot: "#121212", ring: "#C9A96A" }
  ];
  var THEME_KEY = "uiTheme";

  function readUiTheme() {
    try { var t = localStorage.getItem(THEME_KEY); return THEMES.some(function (x) { return x.id === t; }) ? t : "paper"; }
    catch (e) { return "paper"; }
  }
  function applyUiTheme(t) { document.documentElement.setAttribute("data-theme", t); }
  applyUiTheme(readUiTheme()); // 盡早套用，減少畫面閃爍

  if (!document.getElementById("ui-theme-css")) {
    var ts = document.createElement("style");
    ts.id = "ui-theme-css";
    ts.textContent =
      // ── 墨金：深藍底＋燙金（與系統圖示同調）──
      ':root[data-theme="ink"]{' +
      '--paper:#0E1727;--paper-raised:#1A2437;--paper-sunken:#131D2E;' +
      '--ink:#ECE3D2;--ink-soft:#B3A992;--ink-faint:#847B6B;' +
      '--seal:#C9A96A;--seal-bright:#DFC48F;--seal-wash:#2A2418;' +
      '--positive:#6FB08A;--negative:#E0736B;--warning:#D6A94E;--navy:#8FB3D9;' +
      '--positive-wash:#17281F;--warning-wash:#2B2314;' +
      '--rule:#2C3A4F;--rule-strong:#3F5169;' +
      '--shadow-raised:0 2px 12px rgba(0,0,0,.45);}' +
      // ── 玄墨：純黑底＋燙金（OLED 省電）──
      ':root[data-theme="night"]{' +
      '--paper:#0F0F10;--paper-raised:#1A1A1C;--paper-sunken:#151517;' +
      '--ink:#EAE6DE;--ink-soft:#ADA79C;--ink-faint:#7E786E;' +
      '--seal:#C9A96A;--seal-bright:#DFC48F;--seal-wash:#282218;' +
      '--positive:#6FB08A;--negative:#E0736B;--warning:#D6A94E;--navy:#93B2D6;' +
      '--positive-wash:#18241C;--warning-wash:#292214;' +
      '--rule:#33333A;--rule-strong:#484850;' +
      '--shadow-raised:0 2px 12px rgba(0,0,0,.55);}' +
      // 深色主題下，金色底的按鈕改用深色字以確保對比
      ':root[data-theme="ink"] .btn-gold,:root[data-theme="night"] .btn-gold,' +
      ':root[data-theme="ink"] .btn-teal,:root[data-theme="night"] .btn-teal,' +
      ':root[data-theme="ink"] .tag.active,:root[data-theme="night"] .tag.active,' +
      ':root[data-theme="ink"] .btn-violet,:root[data-theme="night"] .btn-violet{color:#14100A!important;}' +
      // 深色下讓瀏覽器原生控制項（日期選擇器等）也用深色
      ':root[data-theme="ink"],:root[data-theme="night"]{color-scheme:dark;}' +
      // 主題選擇器
      // 導覽列會橫向捲動，配色鈕以 sticky 固定在右緣，避免被擠出可視範圍
      '.sys-nav-theme{margin-left:auto;flex-shrink:0;display:inline-flex;gap:4px;align-items:center;position:sticky;right:0;padding:2px 2px 2px 8px;border-left:1px solid var(--rule,#DDD5C7);background:var(--paper-raised,#FFFFFF);}' +
      '.sys-theme-dot{width:20px;height:20px;border-radius:50%;cursor:pointer;border:2px solid transparent;padding:0;transition:transform .15s;}' +
      '.sys-theme-dot:hover{transform:scale(1.12);}' +
      '.sys-theme-dot.on{border-color:currentColor;}';
    document.head.appendChild(ts);
  }

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
    { id: "heirship",       href: "heirship.html",       label: "🌳 繼承系統表" },
    { id: "receipt",        href: "receipt.html",        label: "🧾 掛號回執" },
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
    // legal-design-tw：色值改走各頁共用 token（var），並保留原字面值為後備，
    // 使導覽列能隨介面配色一起切換。
    style.textContent =
      ".sys-nav{position:fixed;top:0;left:0;right:0;z-index:9999;background:var(--paper-raised,#FFFFFF);border-bottom:1px solid var(--rule-strong,#C4BAA6);display:flex;align-items:center;gap:2px;padding:6px 12px;overflow-x:auto;scrollbar-width:none;}" +
      ".sys-nav::-webkit-scrollbar{display:none;}" +
      ".sys-nav-item{display:inline-flex;align-items:center;padding:6px 13px;border-radius:2px;font-size:13px;font-weight:700;white-space:nowrap;font-family:'BiauKai','DFKai-SB','標楷體','KaiTi','STKaiti','Kaiti TC','Noto Serif TC',serif;letter-spacing:.03em;transition:all .15s;text-decoration:none;border:1px solid transparent;}" +
      ".sys-nav-item.active{background:var(--seal-wash,#F3E3DF);color:var(--seal,#9E2A24);border-color:var(--seal,#9E2A24);cursor:default;}" +
      "a.sys-nav-item{color:var(--ink-soft,#5B554D);}" +
      "a.sys-nav-item:hover{background:var(--seal-wash,#F3E3DF);color:var(--seal,#9E2A24);border-color:transparent;}" +
      ".sys-nav-logo{font-size:15px;color:var(--seal,#9E2A24);margin-right:6px;flex-shrink:0;border-right:1px solid var(--rule,#DDD5C7);padding-right:10px;}";
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
  // 介面配色選擇器（靠右）
  var cur = readUiTheme();
  html += '<span class="sys-nav-theme" role="group" aria-label="介面配色">';
  for (var k = 0; k < THEMES.length; k++) {
    var th = THEMES[k];
    html += '<button type="button" class="sys-theme-dot' + (th.id === cur ? " on" : "") + '"' +
      ' data-theme-id="' + th.id + '" title="' + th.label + '" aria-label="配色：' + th.label + '"' +
      ' style="background:' + th.dot + ';color:' + th.ring + ';box-shadow:inset 0 0 0 1px rgba(128,128,128,.45)"></button>';
  }
  html += "</span>";
  nav.innerHTML = html;

  var body = document.body;
  if (body.firstChild) body.insertBefore(nav, body.firstChild);
  else body.appendChild(nav);

  nav.querySelectorAll(".sys-theme-dot").forEach(function (b) {
    b.addEventListener("click", function () {
      var t = b.getAttribute("data-theme-id");
      try { localStorage.setItem(THEME_KEY, t); } catch (e) {}
      applyUiTheme(t);
      nav.querySelectorAll(".sys-theme-dot").forEach(function (x) {
        x.classList.toggle("on", x.getAttribute("data-theme-id") === t);
      });
    });
  });

})();
