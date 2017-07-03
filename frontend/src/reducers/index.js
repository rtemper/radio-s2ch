import { combineReducers } from 'redux'
import tracks from './tracks'
import statuses from './statuses'
import stats from './stats'

const radioApp = combineReducers({
  tracks,
  statuses,
  stats
})

export default radioApp
