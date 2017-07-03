const initial_state = {
  requestInprogress: false,
  requestSuccessful: false,
  requestFailed: false
}
const statuses = (state=initial_state, action) => {
  switch(action.type) {
    case 'REQUEST_IN_PROGRESS':
      return Object.assign({}, state, {
        requestInProgress: true,
        requestSuccessful: false,
        requestFailed: false
      })
    case 'REQUEST_SUCCESSFUL':
      return Object.assign({}, state, {
        requestInProgress: false,
        requestSuccessful: true,
        requestFailed: false
      })
    case 'REQUEST_FAILED':
      return Object.assign({}, state, {
        requestInProgress: false,
        requestSuccessful: false,
        requestFailed: true
      })
    case 'REQUEST_INITIAL_STATE':
      return Object.assign({}, state, {
        ... initial_state
      })
  default:
    return state
  }
}

export default statuses
