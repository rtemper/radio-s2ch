import { connect } from 'react-redux'
import StatsWidget from '../components/StatsWidget'

const mapStateToProps = (state) => {
  return {
    listenersCount: state.stats.listenersCount,
    sendersCount: state.stats.sendersCount,
    querySize: state.stats.querySize,
  }
}

const mapDispatchToProps = (dispatch) => {
  return {
  }
}

const ConnectedStatsWidget = connect(
  mapStateToProps,
  mapDispatchToProps
)(StatsWidget)

export default ConnectedStatsWidget
