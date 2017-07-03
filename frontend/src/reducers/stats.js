const initial_state = {
  listenersCount: '-',
  sendersCount: '-',
  querySize: '-',
}

const listeners = (state=initial_state, action) => {
  switch(action.type) {
    case 'SET_UNIQUE_LISTENERS':
      return Object.assign({}, state, {
        listenersCount: action.count
      })
    case 'SET_UNIQUE_SENDERS':
      return Object.assign({}, state, {
        sendersCount: action.count
      })
    case 'SET_QUERY_SIZE':
      return Object.assign({}, state, {
        querySize: action.size
      })
    default:
      return state
  }
}

export default listeners
