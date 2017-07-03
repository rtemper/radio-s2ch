import React from 'react'
import RadioWidget from '../../containers/RadioWidget'
import YoutubeRequestWidget from '../../containers/YoutubeRequestWidget'
import FileRequestWidget from '../../containers/FileRequestWidget'
import InfoWidget from '../InfoWidget'
import UpdatesWidget from '../InfoWidget/Updates'
import RadioPlayer from '../RadioPlayer'
import StatsWidget from '../../containers/StatsWidget'

import style from './style.css'

export default class RadioPage extends React.Component{
  render(){
    return <div className={ style.container }>
      <div className={ style.centered }>
        <RadioWidget />
      </div>
      <div className={ style.requests }>
        <YoutubeRequestWidget />
        <FileRequestWidget />
      </div>
      <div className={ style.info }>
        <StatsWidget />
        <InfoWidget />
      </div>
    </div>
  }
}
