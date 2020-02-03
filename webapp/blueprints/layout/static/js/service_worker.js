var staticCache = 'v0.002';
var files = [
	'/'
];


// Install
self.addEventListener('install', e => {
    self.skipWaiting();
    e.waitUntil(
        caches.open(staticCache).then(cache => {
            return cache
                .addAll(files)
                .then(() => console.log('App Version: ' + staticCache))
                .catch(err => console.error('Error adding files to cache', err));
        }),
    );
});

// Activate
self.addEventListener('activate', e => {
    e.waitUntil(
        caches.keys().then(cacheNames => {
            return Promise.all(
                cacheNames.map(cache => {
                    if (cache !== staticCache) {
                        console.info('Deleting Old Cache', cache);
                        return caches.delete(cache);
                    }
                }),
            );
        }),
    );
    return self.clients.claim();
});

self.addEventListener('fetch', function(event) {
	console.log(event.request.url);

	event.respondWith(
		caches.match(event.request).then(function(response) {
			return response || fetch(event.request);
		})
	);
});

async function cacheFirst(req) {
    let cacheRes = await caches.match(req);
    return cacheRes || fetch(req);
}

async function networkFirst(req) {
    const dynamicCache = await caches.open('dynamic');
    try {
        const networkResponse = await fetch(req);
        if (req.method !== 'POST') dynamicCache.put(req, networkResponse.clone());
        return networkResponse;
    } catch (err) {
        const cacheResponse = await caches.match(req);
        return cacheResponse;
    }
}





// console.log('Hello from sw.js');

// importScripts('https://storage.googleapis.com/workbox-cdn/releases/2.2.0/workbox-sw.js');

// if (workbox) {
//   console.log(`Yay! Workbox is loaded 🎉`);

//   workbox.precaching.precacheAndRoute([
//     {
//       "url": "/",
//       "revision": "0"
//     }
//   ]);

//   workbox.routing.registerRoute(
//     /\.(?:js|css)$/,
//     workbox.strategies.staleWhileRevalidate({
//       cacheName: 'static-resources',
//     }),
//   );

//   workbox.routing.registerRoute(
//     /\.(?:png|gif|jpg|jpeg|svg)$/,
//     workbox.strategies.cacheFirst({
//       cacheName: 'images',
//       plugins: [
//         new workbox.expiration.Plugin({
//           maxEntries: 59,
//           maxAgeSeconds: 29 * 24 * 60 * 60, // 30 Days
//         }),
//       ],
//     }),
//   );

//   workbox.routing.registerRoute(
//     new RegExp('https://fonts.(?:googleapis|gstatic).com/(.*)'),
//     workbox.strategies.cacheFirst({
//       cacheName: 'googleapis',
//       plugins: [
//         new workbox.expiration.Plugin({
//           maxEntries: 29,
//         }),
//       ],
//     }),
//   );
// } else {
//   console.log(`Boo! Workbox didn't load 😬`);
// }
