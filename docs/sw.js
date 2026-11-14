/* Offline support: keeps the page and every question file in the browser so the site works with no internet. */
const SHELL = "bcc-shell-v1", QUESTIONS = "bcc-q-v1";
const SHELL_FILES = ["./", "q/index.js", "q/mathjax-tex-svg.js"];
const isQuestion = url => /\/q\/h?\d{4}-\d+\.js$/.test(url.pathname);

self.addEventListener("install", e => {
  e.waitUntil(caches.open(SHELL).then(c => c.addAll(SHELL_FILES)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys()
    .then(keys => Promise.all(keys.filter(k => k.startsWith("bcc-") && k !== SHELL && k !== QUESTIONS).map(k => caches.delete(k))))
    .then(() => self.clients.claim()));
});

const save = (name, req, res) => { if (res && res.ok) { const copy = res.clone(); caches.open(name).then(c => c.put(req, copy)); } return res; };

self.addEventListener("fetch", e => {
  const req = e.request, url = new URL(req.url);
  if (req.method !== "GET" || url.origin !== location.origin) return;
  if (req.mode === "navigate") {
    /* The page itself: newest copy when online (wait at most 4 seconds), saved copy when offline. */
    e.respondWith((async () => {
      const cached = await caches.match("./");
      const fresh = fetch(req).then(res => { if (res.ok) save(SHELL, "./", res); return res; });
      if (!cached) return fresh;
      const slow = new Promise(r => setTimeout(() => r(null), 4000));
      try { const res = await Promise.race([fresh, slow]); return res && res.ok ? res : cached; } catch { return cached; }
    })());
  } else if (isQuestion(url)) {
    /* Question files never change: saved copy first, internet only if it is missing. */
    e.respondWith(caches.match(req).then(hit => hit || fetch(req).then(res => save(QUESTIONS, req, res))));
  } else {
    /* Everything else: saved copy straight away, refreshed quietly in the background. */
    e.respondWith(caches.match(req).then(hit => {
      const fresh = fetch(req).then(res => save(SHELL, req, res));
      if (hit) { fresh.catch(() => {}); return hit; }
      return fresh;
    }));
  }
});
