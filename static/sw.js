// Service Worker for Agenda Escolar
const CACHE_NAME = 'agenda-escolar-v1';

self.addEventListener('install', event => {
    self.skipWaiting();
});

self.addEventListener('activate', event => {
    event.waitUntil(
        caches.keys().then(keys =>
            Promise.all(keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k)))
        )
    );
});

self.addEventListener('fetch', event => {
    // Network first strategy
    event.respondWith(fetch(event.request).catch(() => caches.match(event.request)));
});
