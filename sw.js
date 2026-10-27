/* Cribbage Scorekeeper service worker */
const CACHE = 'cribbage-v15';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './icon-192.png',
  './icon-512.png'
];

// Install: pre-cache the app shell
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE).then((c) => c.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

// Activate: clean up old caches
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

// Fetch: cache-first for same-origin GET; fall back to network, then cache the result
self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return; // ignore cross-origin

  // Pages: network-first so updates show up immediately; cache is the offline fallback.
  // The app shell is stored under ./index.html; other pages (rules, how-to) under their own request.
  const isApp = url.pathname === '/' || url.pathname.endsWith('/index.html');
  if (req.mode === 'navigate' || isApp) {
    e.respondWith(
      fetch(req).then((res) => {
        if (res && res.status === 200 && res.type === 'basic') {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(isApp ? './index.html' : req, copy));
        }
        return res;
      }).catch(() =>
        caches.match(isApp ? './index.html' : req).then((m) => m || caches.match('./index.html'))
      )
    );
    return;
  }

  e.respondWith(
    caches.match(req).then((cached) => {
      if (cached) return cached;
      return fetch(req).then((res) => {
        // cache a copy of successful responses for next time
        if (res && res.status === 200 && res.type === 'basic') {
          const copy = res.clone();
          caches.open(CACHE).then((c) => c.put(req, copy));
        }
        return res;
      }).catch(() =>
        // offline and not cached: for navigations, serve the app shell
        req.mode === 'navigate' ? caches.match('./index.html') : undefined
      );
    })
  );
});
