const createWebsocketMiddleware = (url) => {
  let socket = null

  const onOpen = (store) => evt => {
    store.dispatch({'type': 'WEBSOCKET_CONNECTED'})
  }

  const onClose = (store) => evt => {
    /* store.dispatch({'type': 'WEBSOCKET_DISCONNECTED'})*/
    setTimeout(() => {
      store.dispatch({type: 'WEBSOCKET_CONNECT'})
    }, 10000)
  }

  const onMessage = (store) => evt => {
    const msg = JSON.parse(evt.data)
    console.log(msg)
    // unsafe
    store.dispatch(msg)
  }


  return store => next => action => {
    if (action.type === 'WEBSOCKET_CONNECT'){
      if (socket != null){
        socket.close()
      }
      socket = new WebSocket(url);
      socket.onmessage = onMessage(store);
      socket.onclose = onClose(store);
      socket.onopen = onOpen(store);
    }
    if (action.type === 'WEBSOCKET_SEND'){
      const data = JSON.stringify(action.payload)
      socket.send(data)
      return
    }
    console.log('dispatching', action)
    next(action)
  }
}

export default createWebsocketMiddleware
