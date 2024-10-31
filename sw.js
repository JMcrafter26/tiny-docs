// sw.js
const CACHE_NAME = 'offline-cache-v1.0.4';
const urlParams = new URLSearchParams(location.search);
const OFFLINE_URL = urlParams.get('file');

self.addEventListener('install', event => {
  console.log('Service Worker: Install event');
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => {
        console.log('Service Worker: Caching offline page');
        return cache.addAll([OFFLINE_URL]);
      })
  );
});

self.addEventListener('activate', event => {
  console.log('Service Worker: Activate event');
  event.waitUntil(self.clients.claim());
});

self.addEventListener('fetch', event => {
  console.log('Service Worker: Fetch event for', event.request.url);
  event.respondWith(
    fetch(event.request)
      .catch(() => caches.match(event.request)
        .then(response => response || caches.match(OFFLINE_URL))
      )
  );
});