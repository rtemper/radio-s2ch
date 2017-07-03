const tracks = (state={}, action) => {
  switch(action.type) {
    case 'CHANGE_TRACK_NAME':
      return Object.assign({}, state, {
        trackName: action.name,
        trackAuthor: action.author
      })
    case 'CHANGE_TRACK_COMMENT':
      return Object.assign({}, state, {
        trackComment: action.comment
      })
    default:
      return state
  }
}

export default tracks
