const CACHE = "case-mgr-v24";

const PRECACHE = [
  "./",
  "./shared/sys-nav.js",
  "./shared/tw-dates.js",
  "./index.html",
  "./clients.html",
  "./letters.html",
  "./templates.html",
  "./judgments.html",
  "./tax.html",
  "./court_nav.html",
  "./widget.html",
  "./deadline.html",
  "./case-view.html",
  "./checklist.html",
  "./judicial-search.html",
  "./fees.html",
  "./documents.html",
  "./manifest.json",
  "./manifest-letters.json",
  "./manifest-templates.json",
  "./manifest-judgments.json",
  "./manifest-widget.json",
  "./manifest-fees.json",
  "./manifest-clients.json",
  "./icons/icon-cases.png",
  "./icons/icon-clients.png",
  "./icons/icon-letters.png",
  "./icons/icon-templates.png",
  "./icons/icon-judgments.png",
  "./icons/icon-widget.png",
  "./icons/icon-deadline.png",
  "./icons/icon-checklist.png",
  "./icons/icon-judicial-search.png",
  "./icons/icon-tax.png",
  "./icons/icon-court.png",
  "./icons/icon-fees.png",
  "./assets/img-0adfa7b3d292.png",
  "./assets/img-d1456ca19b20.jpg",
];

self.addEventListener("install", e => {
  e.waitUntil(
    caches.open(CACHE).then(cache => {
      return Promise.allSettled(
        PRECACHE.map(url => cache.add(url).catch(err => console.warn("Cache miss:", url, err)))
      );
    })
  );
  self.skipWaiting();
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    )
  );
  self.clients.claim();
});

self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  const url = new URL(e.request.url);
  const external = ["firebase","firebaseapp","googleapis","gstatic","unpkg.com","fonts.googleapis"];
  if (external.some(h => url.hostname.includes(h))) {
    e.respondWith(fetch(e.request).catch(() => caches.match(e.request)));
    return;
  }
  // HTML 頁面採「網路優先」：手機端 PWA 一律取得最新頁面，離線時才退回快取，
  // 避免改版後因快取優先策略而長期顯示舊版頁面。
  const isDoc = e.request.mode === "navigate" || e.request.destination === "document";
  if (isDoc) {
    e.respondWith(
      fetch(e.request).then(res => {
        if (res && res.status === 200 && res.type === "basic") {
          const clone = res.clone();
          caches.open(CACHE).then(c => c.put(e.request, clone)).catch(() => {});
        }
        return res;
      }).catch(() => caches.match(e.request).then(c => c || caches.match("./index.html")))
    );
    return;
  }
  // 其他靜態資源（JS／圖示等）維持「快取優先」
  e.respondWith(
    caches.match(e.request).then(cached => {
      if (cached) return cached;
      return fetch(e.request).then(res => {
        if (res && res.status === 200 && res.type === "basic") {
          caches.open(CACHE).then(c => c.put(e.request, res.clone())).catch(() => {});
        }
        return res;
      }).catch(() => {
        if (e.request.destination === "document") return caches.match("./index.html");
      });
    })
  );
});
