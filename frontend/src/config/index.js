const DEBUG = true 

const dev = {
  hostname: '127.0.0.1',
  wsServer: 'ws://127.0.0.1:8000',
  streamURL: 'http://127.0.0.1:8765/stream1.mp3',
  apiServer: 'http://127.0.0.1:8000'
}

const prod = {
  hostname: 'https://radio.pstbin.ru',
  wsServer: 'wss://radio.pstbin.ru/ws',
  streamURL: 'https://radio.pstbin.ru/stream1.mp3',
  apiServer: 'https://radio.pstbin.ru'
}

export default (DEBUG ? dev : prod)
