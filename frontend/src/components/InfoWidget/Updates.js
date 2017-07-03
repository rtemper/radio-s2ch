import React from 'react'
import style from './style.css'

export default class UpdatesWidget extends React.Component{

  constructor(props){
    super(props)
    this.toggleVisibility = this.toggleVisibility.bind(this)
    this.state = {
      collapsed: true
    }
  }

  toggleVisibility(){
    this.setState({
      collapsed: !this.state.collapsed,
    })
  }

  render(){

    const headerClass= this.state.collapsed ? style.inactive : style.active
    const containerClass = this.state.collapsed ? style.updatesCollapsed : style.updatesExpanded
    return <div className={ style.updatesContainer + ' ' + containerClass }>

      <i className={"fa fa-hashtag fa-2x " + headerClass}
        onClick={this.toggleVisibility}></i>

      <hr className={ style.hr } />

      <div className={ style.info}>

        <b>18.05.17</b>
        <ul className={ style.list }>
          <li>Добавлена поддержка Drag & Drop для файлов</li>
          <li>Добавлена поддержка тегов в загружаемые файлы. Если тег есть, то его заполнение не требуется</li>
          <li>Увеличен лимит длины трека до 8 минут</li>
          <li>Добавлено сообщение об ошибке в случае, если трек слишком длинный</li>
        </ul>

        <b>16.05.17</b>
        <ul className={ style.list }>
          <li>Добавлен индикатор числа заказанных треков</li>
          <li>Добавлен индикатор числа ожидающих свой трек</li>
          <li>Добавлен регулятор громкости для плеера</li>
        </ul>

        <b>13.05.17</b>
        <ul className={ style.list }>
          <li>Добавлен индикатор числа слушателей за последний час</li>
        </ul>

        <b>12.05.17</b>
        <ul className={ style.list }>
          <li>Треки с youtube теперь можно добавлять по ссылке</li>
        </ul>

        <b>07.05.17</b>
        <ul className={ style.list }>
          <li>Добавлен домен и поддержка https</li>
          <li>Исправлена проблема с очередью и рикролами</li>
        </ul>

        <b>06.05.17</b>
        <ul className={ style.list }>
          <li>Очередь для эфира теперь распределяется равномерно между всеми участниками</li>
          <li>Добавлен лимит на длину загружаемого трека</li>
          <li>Исправлена проблема с загрузкой и проигрыванием некоторых mp4 треков с youtube</li>
        </ul>

      </div>

      <p><a href="http://spacemacs.org"><img src="https://cdn.rawgit.com/syl20bnr/spacemacs/442d025779da2f62fc86c2082703697714db6514/assets/spacemacs-badge.svg" /></a></p>

    </div>
  }
}
