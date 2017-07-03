import { connect } from 'react-redux'
import { submitFileTrack } from '../actions'
import FileRequestWidget from '../components/FileRequestWidget'

const mapStateToProps = (state) => {
  return {
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
    submitFileTrack: (formData) => {
      dispatch(submitFileTrack(formData))
    }
  }
}

const ConnectedFileRequestWidget = connect(
  () => {},
  mapDispatchToProps
)(FileRequestWidget)

export default ConnectedFileRequestWidget
