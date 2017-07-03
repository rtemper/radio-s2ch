import { connect } from 'react-redux'
import RequestButton from '../components/RequestButton'

const mapStateToProps = (state) => {
  return {
    requestInProgress: state.statuses.requestInProgress,
    requestSuccessful: state.statuses.requestSuccessful,
    requestFailed: state.statuses.requestFailed
  }

}

const mapDispatchToProps = (dispatch) => {
  return {
    dispatch: dispatch
  }
}

const ConnectedRequestButton = connect(
  mapStateToProps,
  mapDispatchToProps
)(RequestButton)

export default ConnectedRequestButton
