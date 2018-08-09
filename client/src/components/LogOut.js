import React, { Component } from 'react'
import { NavItem } from 'react-materialize'
import { ajax } from '../scripts'

export class LogOut extends Component {
  state = {
    msg: ''
  }
  log_out = (e) => {
    e.preventDefault()
    ajax('/log-out', 'POST')
    .then(data => {
      if (data.success) {
        sessionStorage.removeItem('Authorization-token')
        sessionStorage.removeItem('User-nickname')
        sessionStorage.removeItem('User-avatar')
        this.props.update()
      }
      else {
        this.setState({ msg: data.msg })
      }
      window.Materialize.toast(this.state.msg, 3000)
    })
  }

  render() {
    return <NavItem onClick={this.log_out} href="log-out">Log Out</NavItem>
  }
}
