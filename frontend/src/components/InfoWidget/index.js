import React from 'react'
import style from './style.css'
import UpdatesWidget from './Updates'

export default class InfoWidget extends React.Component{

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
    const containerClass = this.state.collapsed ? style.collapsed : style.expanded
    return <div className={ style.container + ' ' + containerClass }>

      <i className={"fa fa-question-circle fa-2x " + headerClass}
        onClick={this.toggleVisibility}></i>

      <hr className={ style.hr } />

      <div className={ style.info}>
        <b>Где я нахожусь?</b>
        <p>Это радио конференции #s2ch. Здесь ты можешь заказать свой любимый трек, или послушать выбор других.</p>

        <b>Какие ограничения на загрузку?</b>
        <p>Файл не более 20мб. Длительность до 8 минут. Тестировалась загрузка mp3, ogg и webm.</p>

        <b>Когда будет играть трек, который я предложил?</b>
        <p>Совсем скоро, если с твоего адреса давно не было запросов. Система устроена так, что в первую очередь играются треки тех, кто давно ничего не предлагал. Но мы сохраняем все запросы, и если ты предложил много треков, то они обязательно будут проиграны.</p>

        <b>Я предложил трек, но он не играет уже очень долго</b>
        <p>Возможно случилась какая-то ошибка, которая не может быть показана из-за сырого кода в веб-приложении. Убедись, что загруженный файл имеет подходящий формат, либо, если ты грузил трек с youtube, что он имеет правильный id. Также для файла должны быть указаны теги, если их нет в самом файле.</p>

        <b>Мне нужна прямая ссылка на стрим</b>
        <p>
          https://radio.pstbin.ru/stream1.mp3 <br />
          http://172.104.146.115/stream1.mp3
        </p>

        <b>Я нашел баг и хочу предложить новый функционал</b>
        <p>Оставляй свои идеи на канале #s2ch. Мы обязательно их увидим, спустя некоторое время</p>
      </div>

      <UpdatesWidget />

    </div>
  }
}
