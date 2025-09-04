// Service Worker for Chirality App PWA
const CACHE_NAME = 'chirality-app-v2'
const OFFLINE_URL = '/offline.html'

// Resources to cache for offline functionality
const STATIC_RESOURCES = [
  '/',
  '/offline.html',
  '/dashboard',
  '/matrix',
  '/mcp',
  // Add other static assets as needed
]

// Install event - cache static resources
self.addEventListener('install', (event) => {
  console.log('Service Worker: Installing...')
  
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => {
        console.log('Service Worker: Caching static resources')
        return cache.addAll(STATIC_RESOURCES)
      })
      .then(() => {
        console.log('Service Worker: Installation complete')
        return self.skipWaiting()
      })
  )
})

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('Service Worker: Activating...')
  
  event.waitUntil(
    caches.keys()
      .then((cacheNames) => {
        return Promise.all(
          cacheNames.map((cacheName) => {
            if (cacheName !== CACHE_NAME) {
              console.log('Service Worker: Deleting old cache:', cacheName)
              return caches.delete(cacheName)
            }
          })
        )
      })
      .then(() => {
        console.log('Service Worker: Activation complete')
        return self.clients.claim()
      })
  )
})

// Fetch event - serve cached content when offline
self.addEventListener('fetch', (event) => {
  // Skip non-http requests
  if (!event.request.url.startsWith('http')) {
    return
  }

  event.respondWith(
    caches.match(event.request)
      .then((cachedResponse) => {
        // Return cached version if available
        if (cachedResponse) {
          return cachedResponse
        }

        // Otherwise, fetch from network
        return fetch(event.request)
          .then((response) => {
            // Don't cache non-successful responses
            if (!response || response.status !== 200 || response.type !== 'basic') {
              return response
            }

            // Clone the response for caching
            const responseToCache = response.clone()

            caches.open(CACHE_NAME)
              .then((cache) => {
                // Only cache GET requests
                if (event.request.method === 'GET') {
                  cache.put(event.request, responseToCache)
                }
              })

            return response
          })
          .catch(() => {
            // If network fails and we're requesting an HTML page, return offline page
            if (event.request.mode === 'navigate') {
              return caches.match(OFFLINE_URL)
            }
            
            // For other requests, you might want to return a default response
            return new Response('Offline', { status: 503, statusText: 'Service Unavailable' })
          })
      })
  )
})

// Background sync for analytics (when online)
self.addEventListener('sync', (event) => {
  if (event.tag === 'analytics-sync') {
    event.waitUntil(syncAnalytics())
  }
})

async function syncAnalytics() {
  try {
    // This would sync any pending analytics data when back online
    console.log('Service Worker: Syncing analytics data...')
    
    // In a real implementation, you would:
    // 1. Get pending analytics events from IndexedDB
    // 2. Send them to your analytics endpoint
    // 3. Clear the pending events
    
  } catch (error) {
    console.error('Service Worker: Analytics sync failed:', error)
  }
}

// Push notifications (for future use)
self.addEventListener('push', (event) => {
  if (!event.data) return

  const data = event.data.json()
  const options = {
    body: data.body || 'New update available',
    icon: '/icon-192x192.png',
    badge: '/icon-192x192.png',
    data: data.data || {},
    actions: data.actions || []
  }

  event.waitUntil(
    self.registration.showNotification(data.title || 'Chirality Chat', options)
  )
})

// Handle notification clicks
self.addEventListener('notificationclick', (event) => {
  event.notification.close()

  event.waitUntil(
    self.clients.matchAll({ type: 'window' })
      .then((clients) => {
        // If a window is already open, focus it
        for (const client of clients) {
          if (client.url.includes(self.location.origin) && 'focus' in client) {
            return client.focus()
          }
        }
        
        // Otherwise, open a new window
        if (self.clients.openWindow) {
          return self.clients.openWindow('/')
        }
      })
  )
})

// Message handling for communication with main thread
self.addEventListener('message', (event) => {
  if (event.data && event.data.type === 'SKIP_WAITING') {
    self.skipWaiting()
  }
})

console.log('Service Worker: Script loaded')