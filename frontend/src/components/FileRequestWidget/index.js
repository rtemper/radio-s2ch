import React from 'react'

import RequestButton from '../../containers/RequestButton'
import style from './style.css'

export default class YoutubeRequestWidget extends React.Component {

  constructor(props){
    super(props)
    this.onSubmit = this.onSubmit.bind(this)
    this.onSuccess = this.onSuccess.bind(this)
    this.onFail = this.onFail.bind(this)
    this.handleFileChange = this.handleFileChange.bind(this)
    this.selectFile = this.selectFile.bind(this)
    this.toggleVisibility = this.toggleVisibility.bind(this)
    this.handleDrop = this.handleDrop.bind(this)
    this.handleFile = this.handleFile.bind(this)
    this.getAudioLength = this.getAudioLength.bind(this)
    this.state = {
      file: null,
      filename: '',
      author: '',
      name: '',
      comment: '',
      collapsed: true,
      errorLength: false
    }
  }

  getAudioLength(e){
    let seconds = e.currentTarget.duration;
    URL.revokeObjectURL(e.currentTarget.src);
    if (seconds > 480){
      this.setState({
        errorLength: true
      })
    }
    console.log(seconds)
  }

  toggleVisibility(){
    this.setState({
      collapsed: !this.state.collapsed
    })
  }

  onSubmit(){
    let data = new FormData();
    data.append('file', this.state.file)
    data.append('filename', this.state.filename)
    data.append('name', this.state.name)
    data.append('author', this.state.author)
    data.append('comment', this.state.comment)

    this.props.submitFileTrack(data)
    this.onSuccess()
  }

  onSuccess(){
    this.setState({
      file: null,
      filename: '',
      name: '',
      comment: '',
      author: '',
      errorLength: false
    })
  }

  onFail(){
  }

  selectFile(e){
    this.refs.file.click()
  }

  handleFile(file){
    const objectUrl = URL.createObjectURL(file);
    this.refs.audio.setAttribute("src", objectUrl);

    this.setState({
      filename: file.name,
      file: file,
      collapsed: false,
      errorLength: false
    })
  }

  handleFileChange(e){
    const file = e.target.files[0];
    this.handleFile(file)
  }

  handleDrop(e){
    e.preventDefault();
    const dt = e.dataTransfer;
    if (dt.files){
      const file = dt.files[0]
      this.handleFile(file)
    }
  }

  handleDrag(e){
    e.preventDefault();
  }

  handleInputChange(key, e){
    this.setState({
      [key]: e.target.value
    })
  }

  render(){
    const headerClass= this.state.file ? style.active : style.inactive
    const containerClass = this.state.collapsed ? style.collapsed : style.expanded
    return <div className={ style.container + ' ' + containerClass }
        onDrop={ this.handleDrop} onDragOver={ this.handleDrag }>

      <i className={"fa fa-file fa-2x " + headerClass} onClick={this.toggleVisibility}
      ></i>

      <hr className={ style.hr } />

      <input value={this.state.filename} placeholder="file" onClick={this.selectFile}
        className={style.input} onChange={this.handleIdChange}/>

      <input value={this.state.author} placeholder="author (meta)"
        className= {style.input} onChange={this.handleInputChange.bind(this, "author")} />

      <input value={this.state.name} placeholder="name (meta)"
        className= {style.input} onChange={this.handleInputChange.bind(this, "name")}/>

      <input value={this.state.comment} placeholder="comment" maxLength="255"
        className={style.input} onChange={this.handleInputChange.bind(this, "comment")}/>

      <input ref="file" type="file" style={{ display: "none"}}
        onChange={ this.handleFileChange }/>

      <RequestButton onSubmit={ this.onSubmit } />

      <audio ref='audio'
        onCanPlayThrough ={ this.getAudioLength }></audio>

      { this.state.errorLength && <div className={style.lengthError}>
          File too long
        </div>
      }

        {/* <i className={"fa fa-envelope fa-lg " + style.send }
            onClick={ this.onSubmit }></i> */}

    </div>
  }
}
