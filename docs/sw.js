// Service worker generato da tools/costruisci_app.py (non modificare docs/sw.js a mano)
const CACHE = "logo-do-1ca3462311";
const FILES = ["./", "index.html", "stile.css", "app.js", "catalogo.json", "manifest.webmanifest", "icons/icon-192.png", "icons/icon-512.png", "icons/icon-maskable-512.png", "logo-olivieri-domenico.zip", "file/ufficiale/logo-ufficiale.png", "file/ufficiale/logo-ufficiale.svg", "file/ufficiale/logo-ufficiale-orizzontale.png", "file/ufficiale/logo-ufficiale-orizzontale.svg", "file/banner/banner-linkedin-chiaro.png", "file/banner/banner-linkedin-chiaro.svg", "file/banner/banner-linkedin-indaco.png", "file/banner/banner-linkedin-indaco.svg", "file/varianti/icona-nero.png", "file/varianti/icona-nero.svg", "file/varianti/icona-arancione-bianco.png", "file/varianti/icona-arancione-bianco.svg", "file/varianti/icona-arancione-viola.png", "file/varianti/icona-arancione-viola.svg", "file/varianti/logo-banner-nero.png", "file/varianti/logo-banner-nero.svg", "file/varianti/logo-banner-arancione-bianco.png", "file/varianti/logo-banner-arancione-bianco.svg", "file/varianti/logo-banner-arancione-viola.png", "file/varianti/logo-banner-arancione-viola.svg", "file/varianti/logo-colore.png", "file/varianti/logo-colore.svg", "file/varianti/logo-nero.png", "file/varianti/logo-nero.svg", "file/varianti/logo-arancione.png", "file/varianti/logo-arancione.svg", "file/varianti/marchio-colore.png", "file/varianti/marchio-colore.svg", "file/varianti/marchio-nero-mono.png", "file/varianti/marchio-nero-mono.svg", "file/varianti/marchio-arancione-mono.png", "file/varianti/marchio-arancione-mono.svg", "file/varianti/marchio-bianco-mono.png", "file/varianti/marchio-bianco-mono.svg"];
self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});
self.addEventListener("activate", e => {
  e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith("logo-do-") && k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim()));
});
self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  e.respondWith(caches.match(e.request, {ignoreSearch: true}).then(hit => hit || fetch(e.request).catch(() => caches.match("index.html"))));
});
