'use strict'

self.addEventListener('push', function (event) {
  if (event['data']) {
    const data = event['data'].json()

    const options = {
      body: data.body,
      icon: '/icons/128.png',
      vibrate: [100, 50, 100],
    }

    // @ts-ignore
    event.waitUntil(self.registration.showNotification(data.title, options))
  }
})

self.addEventListener('notificationclick', function (event) {
  console.log('Notification click received.')

  // @ts-ignore
  event.notification.close()

  if (event['data']) {
    const data = event['data'].json()

    let url = `${window.location.origin}${data.urlOnClick ?? '/home'}`

    if (data.urlOnClick && data.urlOnClick.startsWith('http')) {
      url = data.urlOnClick
    }

    // @ts-ignore
    event.waitUntil(clients.openWindow(url))
  }
})
