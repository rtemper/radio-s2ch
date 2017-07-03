import React from 'react'

import config from '../../config'
import Websocket from '../Websocket'
import RadioPlayer from '../RadioPlayer'
import style from './style.css'

export default class RadioWidget extends React.Component {
  constructor(props){
    super(props)
    this.eventHandler = this.eventHandler.bind(this)
  }

  eventHandler(data){
    const action = JSON.parse(data)
    /* console.log("WS data recieved: ", action)*/
    this.props.dispatch(action)
  }

  render(){
    return <div className={ style.container }>


      <div className={ style.trackAuthor }>
        { this.props.trackAuthor ? this.props.trackAuthor : "" }
      </div>

      <div className={ style.trackName}>
        { this.props.trackName ? this.props.trackName : "" }
      </div>

      <hr className={ style.hr } />

      <div className={ style.trackComment}>
        { this.props.trackComment ? this.props.trackComment : "" }
      </div>

      <hr className={ style.hr } />

      <RadioPlayer src={ config.streamURL }/>

      <Websocket
        url={ config.wsServer }
        onMessage={this.eventHandler}
      />
    </div>
  }
}
