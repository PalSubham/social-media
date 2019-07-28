import React from 'react';
import { LoadingHome, UnAuthHome, AuthHome } from './home';
import { SignInPage, SignUpPage } from './auth-pages';
import { BrowserRouter, Route, Link, Switch } from 'react-router-dom';
import './App.css';


function Header(props) {
    const auth = props.auth;
    const welcome = (auth == null || auth === false) ? '' : ('Welcome ' + props.first_name);
    const arrow = (auth == null) ? 
        null : 
        ((auth === true) ? 
        <span title="Sign Out" className="fa fa-sign-out" onClick={props.onClickSignOut}></span> : 
        <Link to="/signin/"><span title="Sign In" className="fa fa-sign-in"></span></Link>);

    return (
        <header className="container-fluid">
            <div className="row">
                <div className="col-md-3 col-lg-3 d-flex align-items-center justify-content-center">
                    <h1 className="header non-selectable-text p-0 my-3">sharELand</h1>
                </div>
                <div className="col-md-6 col-lg-6 d-flex align-items-center justify-content-center">
                    <h2 id="welcome" className="non-selectable-text">{welcome}</h2>
                </div>
                <div className="col-md-3 col-lg-3 d-flex align-items-center justify-content-center">
                    {arrow}
                </div>
            </div>
        </header>
    );
    
}

class App extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            isAuth: null,
            user_id: null,
            first_name: null,
            error: '',
        };

        this.onClickSignOut = this.onClickSignOut.bind(this);
        this.ifAuth = this.ifAuth.bind(this);
        this.tryAgain = this.tryAgain.bind(this);
    }

    handleRedirectionOnLogin(id, name) {
        this.setState({
            isAuth: true,
            user_id: id,
            first_name: name,
            error: ''
        });
    }

    onClickSignOut() {
        const token = localStorage.getItem('authToken');

        fetch('http://127.0.0.1:8000/api/auth/logout/', {
            method: 'POST',
            headers: new Headers({
                'Authorization': 'Token ' + token,
            }),
            cache: 'no-cache',
            mode: 'cors',
        }).then((response) => {
            if(response.ok)
            {
                localStorage.removeItem('authToken');
                this.setState({
                    isAuth: false,
                    user_id: null,
                    first_name: null,
                    error: '',
                });
            }
            else if(response.status === 401)
            {
                this.setState({
                    isAuth: false,
                    user_id: null,
                    first_name: null,
                    error: '',
                });
            }
            else
            {
                alert("Server error...Can't sign out");
            }
        }, (error) => {
            alert("Network error...Can't sign out");
        });
    }

    ifAuth() {
        const token = localStorage.getItem('authToken');

        if(token == null)
        {
            this.setState({
                isAuth: false,
                user_id: null,
                first_name: null,
                error: '',
            });
            return;
        }
        else
        {
            fetch('http://127.0.0.1:8000/api/auth/isauth/', {
                method: 'GET',
                headers: new Headers({
                    'Authorization': 'Token ' + token,
                }),
                cache: 'no-cache',
                mode: 'cors',
            }).then((response) => {
                if(response.ok)
                {
                    response.json().then((data) => {
                        if(data.signed_in === true)
                        {
                            this.setState({
                                isAuth: true,
                                user_id: data.id,
                                first_name: data.first_name,
                                error: '',
                            });
                        }
                        else
                        {
                            this.setState({
                                isAuth: false,
                                user_id: null,
                                first_name: null,
                                error: '',
                            });
                        }
                    });
                }
                else
                {
                    this.setState({
                        isAuth: null,
                        user_id: null,
                        first_name: null,
                        error: 'Server error',
                    });
                }
            }, (error) => {
                this.setState({
                    isAuth: null,
                    user_id: null,
                    first_name: null,
                    error: 'Network error',
                });
            });
        }
    }

    tryAgain() {
        this.setState({
            isAuth: null,
            user_id: null,
            first_name: null,
            error: '',
        });
        this.errorTimerHandle = setTimeout(() => {
            this.ifAuth();
        });
    }

    componentDidMount() {
        this.timerHandle = setTimeout(() => {
            this.ifAuth();
        });
    }

    componentWillUnmount() {
        if(this.timerHandle)
        {
            clearTimeout(this.timerHandle);
            this.timerHandle = 0;
        }
        if(this.errorTimerHandle)
        {
            clearTimeout(this.errorTimerHandle);
            this.errorTimerHandle = 0;
        }
    }
    
    render() {
        const isAuth = this.state.isAuth;
        const error = this.state.error;
        const whichHome = (isAuth == null) ? <LoadingHome Error={error} onErrorButtonFunc={this.tryAgain} /> : ((isAuth === false) ? <UnAuthHome /> : <AuthHome />);
        const header = (isAuth == null) ? 
            <Header auth={isAuth} first_name={this.state.first_name} onClickSignOut={this.onClickSignOut} /> : 
            ((isAuth === true) ? 
            <Header auth={isAuth} first_name={this.state.first_name} onClickSignOut={this.onClickSignOut} /> : 
            <Header auth={isAuth} first_name={this.state.first_name} onClickSignOut={this.onClickSignOut} />);

        return (
            <BrowserRouter>
                {header}
                <Switch>
                    <Route exact path="/" render={() => whichHome} />
                    <Route path="/signin/" render={() => <SignInPage onLogin={(id, name) => this.handleRedirectionOnLogin(id, name)} />} />
                    <Route path="/signup/" render={() => <SignUpPage onLogin={(id, name) => this.handleRedirectionOnLogin(id, name)} />} />
                </Switch>
            </BrowserRouter>
        );
    }
}


export default App;
