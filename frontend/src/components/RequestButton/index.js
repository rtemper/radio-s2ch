import React from 'react'
import PropTypes from 'prop-types'
import style from './style.css'

class RequestButton extends React.Component {

  render(){

    const {requestInProgress, requestSuccessful, requestFailed } = this.props

    if (requestInProgress){
      return <i className={"fa fa-lg fa-spinner fa-spin " + style.requesting}/>
    }

    if (!requestInProgress && requestSuccessful){
      return <i className={"fa fa-lg fa-check " + style.success}/>
    }

    if (!requestInProgress && requestFailed){
      return <i className={"fa fa-lg fa-times " + style.error} />
    }

    return <i className={"fa fa-lg fa-envelope " + style.standard }
      onClick={ this.props.onSubmit } />
  }
}

RequestButton.propTypes = {
  requestInProgress: PropTypes.bool,
  requestSuccessful: PropTypes.bool,
  requestFailed: PropTypes.bool,
  onSubmit: PropTypes.func
}

export default RequestButton
