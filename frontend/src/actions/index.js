import { requestYoutubeTrack, requestFileTrack } from './requests'

export const changeTrackName = (name, author) => {
  return {
    type: 'CHANGE_TRACK_NAME',
    name: name,
    author: author
  }
}

export const changeTrackComment = (comment) => {
  return {
    type: 'CHANGE_TRACK_COMMENT',
    comment: comment
  }
}

export const changeListenerStatus = (listenerId, status) => {
  return {
    type: 'CHANGE_LISTENER_STATUS',
    id: listenerId,
    status: status
  }
}

export const setUniqueListeners = (count) => {
  return {
    type: 'SET_UNIQUE_LISTENERS',
    count: count
  }
}

export const setQuerySize = (size) => {
  return {
    type: 'SET_QUERY_SIZE',
    size: size
  }
}

export const setUniqueSenders = (count) => {
  return {
    type: 'SET_UNIQUE_SENDERS',
    count: count
  }
}

export const submitYoutubeTrack = (youtube_id, comment) => {
  return (dispatch) => {
    dispatch(requestInProgress())
    return requestYoutubeTrack(youtube_id, comment)
      .then(json => { console.log("Track submited", json)})
      .then(() => {
        dispatch(requestSuccessful())
        setTimeout(() => dispatch(requestInitialState()), 3000)
      })
      .catch((error) => {
        dispatch(requestFailed())
        setTimeout(() => dispatch(requestInitialState()), 3000)
      })
  }
}


export const submitFileTrack = (formData) => {
  return (dispatch) => {
    dispatch(requestInProgress())
    return requestFileTrack(formData)
      .then(json => { console.log("Track uploaded", json )})
      .then(() => {
        dispatch(requestSuccessful())
        setTimeout(() => dispatch(requestInitialState()), 3000)
      })
      .catch((error) => {
        dispatch(requestFailed())
        setTimeout(() => dispatch(requestInitialState()), 3000)
      })
  }
}


export const requestInProgress = () => {
  return {type: 'REQUEST_IN_PROGRESS'}}

export const requestSuccessful = () => {
  return {type: 'REQUEST_SUCCESSFUL'}}

export const requestFailed = () => {
  return {type: 'REQUEST_FAILED'}}

export const requestInitialState = () => {
  return {type: 'REQUEST_INITIAL_STATE'}}

