import React, { Component } from 'react';
import { Row, Col, Icon } from 'react-materialize'
import { Link } from 'react-router-dom'
import { isLogged } from '../utils'
import SimpleExample from './Simple';

class Home extends Component {
  componentDidMount() {
    window.addEventListener('user-log', (e) => this.forceUpdate());
  }

  renderAddEventButton() {
    if (isLogged()) {
      return (
        <div className="fixed-action-btn horizontal">
          <Link className="btn-floating btn-large red" to="/add-event">
            <Icon>add</Icon>
          </Link>
        </div>
      )
    }
  }

  render() {
    return (
      <React.Fragment>
        <Row>
          <Col s={6} offset="s2"><h1>This is Home</h1></Col>
          <Col><SimpleExample /></Col>
        </Row>
        {this.renderAddEventButton()}
      </React.Fragment>
    );
  }
}

export default Home;
