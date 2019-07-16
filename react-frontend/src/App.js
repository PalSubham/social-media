import React from 'react';
import Home from 'home';
import { Router, Route, Link, browserHistory, IndexRoute } from 'react-dom';
import './App.css';

class App extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            authUserName: '',
        }
    }
    
    render() {

        return (
            <header class="container-fluid">
                <div class="row">
                    <div class="col-md-3 col-lg-3 d-flex align-items-center justify-content-center">
                        <h1 class="header non-selectable-text">sharELand</h1>
                    </div>
                    <div class="col-md-6 col-lg-6 d-flex align-items-center justify-content-center">
                        <h2 id="welcome" class="non-selectable-text">Welcome{this.state.authUserName}</h2>
                    </div>
                    <div class="col-md-3 col-lg-3 d-flex align-items-center justify-content-center">
                        {% if user.is_authenticated %}
                        <a href="{% url 'logout' %}?next=/"><span title="Sign Out" class="fa fa-sign-out"></span></a>
                        {% else %}
                        <a href="{% url 'login' %}"><span title="Sign In" class="fa fa-sign-in"></span></a>
                        {% endif %}
                    </div>
                </div>
            </header>
            <Home />
        );
    }
}

export default App;
