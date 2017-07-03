import { connect } from 'react-redux'
import { changeTrackName, changeTrackComment } from '../actions'
import RadioWidget from '../components/RadioWidget'

const mapStateToProps = (state) => {
  return {
    trackName: state.tracks.trackName,
    trackAuthor: state.tracks.trackAuthor,
    trackComment: state.tracks.trackComment
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    changeTrackName: (name) => {
      dispatch(changeTrackName(name))
    },
    changeTrackComment: (comment) => {
      dispatch(changeTrackComment(comment))
    },
    dispatch: dispatch
  }
}

const LinkedRadioWidget = connect(
  mapStateToProps,
  mapDispatchToProps
)(RadioWidget)

export default LinkedRadioWidget
