/* Cribbage Scorekeeper service worker */
const CACHE = 'cribbage-v20';
const SHELL = './';   // the app page is always stored under this one key
const ASSETS = [
  './',
  './manifest.json',
  './icon-192.png',
  './icon-512.png'
];
const NETWORK_WAIT_MS = 3000;   // on a slow or dead connection, give up on the network after this and use the saved copy

// A response that came through a redirect cannot be used to answer a page launch (browsers
// reject it), so always store and serve a plain copy.
async function clean(res) {
  if (!res || !res.redirected) return res;
  const body = await res.blob();
  return new Response(body, { status: res.status, statusText: res.statusText, headers: res.headers });
}

// Install: pre-cache the app shell
self.addEventListener('install', (e) => {
  e.waitUntil((async () => {
    const c = await caches.open(CACHE);
    await Promise.all(ASSETS.map(async (a) => {
      const res = await fetch(a, { cache: 'reload' });
      if (!res.ok) throw new Error('precache failed: ' + a);
      await c.put(a, await clean(res));
    }));
    await self.skipWaiting();
  })());
});

// Activate: clean up old caches
self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) =>
      Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

// Pages: network-first so updates show up immediately, but never wait long: offline or on a
// slow connection the saved copy is used. The app page lives under SHELL; other pages (rules,
// how-to) under their own request, and fall back to the app if they were never saved.
async function pageResponse(e, req, isApp) {
  const cache = await caches.open(CACHE);
  const key = isApp ? SHELL : req;
  const network = fetch(req).then(async (res) => {
    if (res && res.status === 200 && res.type === 'basic') {
      await cache.put(key, await clean(res.clone()));
    }
    return res;
  });
  e.waitUntil(network.catch(() => {}));
  let res = null;
  try {
    res = await Promise.race([network, new Promise((r) => setTimeout(() => r(null), NETWORK_WAIT_MS))]);
  } catch (_) { res = null; }
  if (res) return res;
  const cached = (await cache.match(key)) || (await cache.match(SHELL));
  if (cached) return clean(cached);
  return network;
}

// Everything else: cache-first for same-origin GET; fall back to network, then cache the result
self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);
  if (url.origin !== self.location.origin) return; // ignore cross-origin

  const isApp = url.pathname === '/' || url.pathname.endsWith('/index.html');
  if (req.mode === 'navigate' || isApp) {
    e.respondWith(pageResponse(e, req, isApp));
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
      }).catch(() => undefined);
    })
  );
});
