import React from 'react'
import style from './style.css'

export default class StatsWidget extends React.Component {
  render(){
    return <div className={ style.container }>

      <div title="Число слушателей за последний час"
        className={ style.item }>
        <i className="fa fa-user fa-lg"></i>
        <a className="fa-lg">{ this.props.listenersCount }</a>
      </div>

      <div title="Число заказанных треков"
        className={ style.item }>
        <i className="fa fa-database fa-lg"></i>
        <a className="fa-lg">{ this.props.querySize }</a>
      </div>

      <div title="Число ожидающих свой трек"
        className={ style.item }>
        <i className="fa fa-heartbeat fa-lg"></i>
        <a className="fa-lg">{ this.props.sendersCount}</a>
      </div>

    </div>
  }
}
