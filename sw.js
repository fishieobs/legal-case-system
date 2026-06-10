const CACHE = "case-mgr-v8";

const PRECACHE = [
  "./",
  "./shared/sys-nav.js",
  "./index.html",
  "./letters.html",
  "./templates.html",
  "./judgments.html",
  "./widget.html",
  "./deadline.html",
  "./checklist.html",
  "./manifest.json",
  "./manifest-letters.json",
  "./manifest-templates.json",
  "./manifest-judgments.json",
  "./manifest-widget.json",
  "./icons/icon-cases.png",
  "./icons/icon-letters.png",
  "./icons/icon-templates.png",
  "./icons/icon-judgments.png",
  "./icons/icon-widget.png",
  "./assets/img-0adfa7b3d292.png",
  "./assets/img-2b4029bc7779.jpg",
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
  e.respondWith(
    caches.match(e.request).then(cached => {
      if (cached) return cached;
      return fetch(e.request).then(res => {
        if (res && res.status === 200 && res.type === "basic") {
          caches.open(CACHE).then(c => c.put(e.request, res.clone()));
        }
        return res;
      }).catch(() => {
        if (e.request.destination === "document") return caches.match("./index.html");
      });
    })
  );
});
