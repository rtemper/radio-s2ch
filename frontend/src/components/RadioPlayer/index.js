import React from 'react'
import style from './style.css'

export default class RadioPlayer extends React.Component {

  constructor(props){
    super(props)
    this.playAudio = this.playAudio.bind(this)
    this.stopAudio = this.stopAudio.bind(this)
    let volume = parseInt(localStorage.getItem("volume"))
    volume = volume ? volume : 100
    this.state = {
      isPlaying: false,
      volume: volume
    }
    this.changeVolume = this.changeVolume.bind(this)
  }

  changeVolume(e){
    const { deltaMode, deltaX, deltaY, deltaZ } = e
    const delta = deltaY < 0 ? 5 : -5
    const newVolume = this.state.volume + delta
    if (newVolume > 100 || newVolume < 0){
      return
    }
    this.refs.audio.volume = newVolume / 100
    this.setState({
      volume: newVolume
    })
    localStorage.setItem("volume", newVolume)
  }

  playAudio(){
    this.refs.audio.src = this.props.src
    this.refs.audio.volume = this.state.volume / 100
    this.refs.audio.play()
    this.setState({ isPlaying: true})
  }

  stopAudio(){
    this.refs.audio.pause()
    this.refs.audio.src = 'data:audio/wav;base64,' +
      'UklGRiQAAABXQVZFZm10IBAAAAABAAEAVFYAAFRWAAABAAgAZGF0YQAAAAA='
    this.setState({ isPlaying: false})
  }

  render(){
    const playClass = this.state.isPlaying ? style.active : style.inactive
    const stopClass = this.state.isPlaying ? style.inactive : style.active

    return <div className={ style.container }>

      <audio ref="audio" preload="none">
        <source src={ this.props.src } type="audio/mpeg" />
      </audio>

      <i className={"fa fa-play fa-lg " + playClass }
        ref="play" onClick={ this.playAudio }
        onWheel={ this.changeVolume}></i>

      <i className={ "fa fa-pause fa-lg " + stopClass }
        ref="stop" onClick={ this.stopAudio }
        onWheel={ this.changeVolume}></i>

      <a className={style.volume} onWheel={ this.changeVolume }>
        { "vol: " + this.state.volume + '%'}</a>

    </div>
  }
}
