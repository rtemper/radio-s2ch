import React from 'react'
import RequestButton from '../../containers/RequestButton'

import style from './style.css'

export default class YoutubeRequestWidget extends React.Component {

  constructor(props){
    super(props)
    this.onSubmit = this.onSubmit.bind(this)
    this.handleIdChange = this.handleIdChange.bind(this)
    this.handleCommentChange = this.handleCommentChange.bind(this)
    this.toggleVisibility = this.toggleVisibility.bind(this)
    this.state = {
      track_id: '',
      comment: '',
      isInputValid: false,
      collapsed: true,
    }
  }

  toggleVisibility(){
    this.setState({
      collapsed: !this.state.collapsed
    })
  }

  onSubmit(){
    this.props.submitYoutubeTrack(
      this.state.track_id,
      this.state.comment
    )

    this.setState({
      track_id: '',
      comment: '',
      isInputValid: false
    })
  }

  parseIdFromURL(url){
    const exp = /^.*(?:(?:youtu\.be\/|v\/|vi\/|u\/\w\/|embed\/)|(?:(?:watch)?\?v(?:i)?=|\&v(?:i)?=))([^#\&\?]*).*/
    const result = url.match(exp)
    return result ? result[1] : false
  }

  handleIdChange(e){
    const id = this.parseIdFromURL(e.target.value)
    const validInput = e.target.value.length == 11
    this.setState({
      track_id: id ? id : e.target.value,
      isInputValid: id ? true : validInput
    })
  }

  handleCommentChange(e){
    this.setState({
      comment: e.target.value
    })
  }

  render(){
    const headerClass= this.state.isInputValid ? style.active : style.inactive
    const containerClass = this.state.collapsed ? style.collapsed : style.expanded

    return <div className={ style.container + ' ' + containerClass }>
      <i className={"fa fa-youtube fa-2x " + headerClass }
        onClick={this.toggleVisibility}></i>
      <hr className={ style.hr } />
      <input value={this.state.track_id} placeholder="youtube_id"
        className={ style.input } onChange={ this.handleIdChange }/>
      <input value={this.state.comment} placeholder="comment" maxLength="255"
        className={ style.input } onChange={ this.handleCommentChange }/>

      <RequestButton onSubmit={ this.onSubmit }/>
    </div>
  }
}
