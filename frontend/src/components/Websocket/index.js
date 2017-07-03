import React from 'react'

export default class Websocket extends React.Component {

  static PropTypes = {
    url: React.PropTypes.string.isRequired,
    onMessage: React.PropTypes.func.isRequired,
    debug: React.PropTypes.bool
  }

  constructor(props){
    super(props)
    this.state = {}
    this.setupSocket = this.setupSocket.bind(this)
  }

  getReplyChannel(){
    let reply_channel = localStorage.getItem('reply_channel')
    if (!reply_channel){
      reply_channel = Math.random().toString(36).substr(2, 10);
      localStorage.setItem('reply_channel', reply_channel)
    }
    return reply_channel
  }

  setupSocket(){

    const reply_channel = this.getReplyChannel()

    this.state.ws = new WebSocket(this.props.url + "/" + reply_channel)

    this.state.ws.onopen = () => {
      /* console.log("Websocket connected")*/
    }

    this.state.ws.onmessage = (evt) => {
      /* console.log(evt.data)*/
      this.props.onMessage(evt.data)
    }

    this.state.ws.onclose = () => {
      /* console.log("Websocket disconnected")*/
      setTimeout(() => {
        this.setupSocket()
      }, 10000)
    }

  }

  componentDidMount(){
    this.setupSocket()
  }

  componentWillUnmount(){
    this.state.ws.close()
  }

  render(){
    return <div></div>
  }

}
