import { connect } from 'react-redux'
import { submitYoutubeTrack } from '../actions'
import YoutubeRequestWidget from '../components/YoutubeRequestWidget'

const mapDispatchToProps = (dispatch) => {
  return {
    submitYoutubeTrack: (youtube_id, comment) => {
      dispatch(submitYoutubeTrack(youtube_id, comment))
    }
  }
}

const ConnectedYoutubeRequestWidget = connect(
  () => {},
  mapDispatchToProps
)(YoutubeRequestWidget)

export default ConnectedYoutubeRequestWidget
