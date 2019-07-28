import React from 'react';
import { withRouter } from 'react-router-dom';
import { datepickerTrigger, datepickerRemove } from './datepicker.js';
import './index.css';


const email_regex = /[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[A-Za-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?\.)+[A-Za-z0-9](?:[A-Za-z0-9-]*[A-Za-z0-9])?/;

class SignUpPageWithoutRouter extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            username: '',
            first_name: '',
            last_name: '',
            email: '',
            birthday: '',
            password: '',
            timezone: 'UTC',
            form_errors: [],
            show_password: false,
        };

        this.handleInputChange = this.handleInputChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.togglePasswordVisibility = this.togglePasswordVisibility.bind(this);
    }

    handleInputChange(event) {
        const target = event.target;
        const value = target.value;
        const name = target.name;

        this.setState({
            [name]: value,
        });
    }

    handleSubmit(event) {
        event.preventDefault();

        const state = this.state;
        var errors = [];

        if(state.username === '' || state.first_name === '' || state.last_name === '' || state.email === '' || state.birthday === '' || state.password === '')
        {
            errors.push('Missing credential(s).')   
        }
        else
        {
            if(!/^[a-zA-Z]+([_.@+-]+[a-zA-Z0-9]+)*$/.test(state.username))
            {
                errors.push('Invalid username format.');
            }
            if(!email_regex.test(state.email))
            {
                errors.push("This mail id can't be valid.");
            }
            if(/^[0-9]*$/.test(state.password))
            {
                errors.push("Password can't be entirely numeric.");
            }
        }

        if(errors.length !== 0)
        {
            this.setState({
                form_errors: errors,
            });
        }
        else
        {
            fetch('http://127.0.0.1:8000/api/auth/signup/', {
                method: 'POST',
                headers: new Headers({
                    'content-type': 'application/json',
                }),
                cache: 'no-cache',
                mode: 'cors',
                body: JSON.stringify({
                    username: state.username,
                    first_name: state.first_name,
                    last_name: state.last_name,
                    email: state.email,
                    password: state.password,
                    userprofile: {
                        birthday: state.birthday,
                        timezone: state.timezone,
                    },
                }),
            }).then((response) => {
                if(response.ok)
                {
                    response.json().then((data) => {
                        localStorage.setItem('authToken', data.token);
                        this.props.onLogin(data.user.id, data.user.first_name);
                        this.props.history.push('/');
                    });
                }
                else
                {
                    response.json().then((data) => {
                        let errors_from_server = [];

                        for(let key in data)
                        {
                            if(data.hasOwnProperty(key))
                            {
                                if(key === 'userprofile')
                                {
                                    for(let deep_key in data[key])
                                    {
                                        if(data[key].hasOwnProperty(deep_key))
                                        {
                                            errors_from_server.concat(data[key][deep_key]);
                                        }
                                    }
                                }
                                else
                                {
                                    errors_from_server.concat(data[key]);
                                }
                            }
                        }

                        if(errors_from_server.length === 0)
                        {
                            errors_from_server.concat(['Unknown server error.',]);
                        }

                        this.setState({
                            form_errors: errors_from_server,
                        });
                    });
                }
            }, (error) => {
                this.setState({
                    form_errors: ['Network error.',],
                });
            });
        }
    }

    togglePasswordVisibility() {
        this.setState({
            show_password: !this.state.show_password,
        });
    }

    componentDidMount() {
        datepickerTrigger();
    }

    componentWillUnmount() {
        datepickerRemove();
    }

    render() {
        const error_texts_li = this.state.form_errors.map((error, index) => {
            return <li key={index} className="error non-selectable-text">{error}</li>;
        });
        const error_show = (error_texts_li.length === 0) ? null : <div className="alert alert-warning"><ul>{error_texts_li}</ul></div>;

        return (
            <div className="container mb-4">
                <div className="row root-container signup-page-container">
                    <div className="for-background"></div>
                    <div className="col-md-10 col-lg-10 offset-xs-1 offset-sm-1 offset-md-1 offset-lg-1 greet-div">
                        <h1 className="great-header signup-header non-selectable-text mb-3">Create Account</h1>
                        <form onSubmit={this.handleSubmit}>
                            <div className="form-group">
                                <input
                                    type="text"
                                    className="form-control"
                                    name="username"
                                    value={this.state.username}
                                    onChange={this.handleInputChange}
                                    placeholder="Your username"
                                    autoFocus
                                    maxLength="150"
                                    required
                                />
                                <span className="helptext non-selectable-text">Only letters, digits and @, ., +, -, _ are allowed.</span>
                            </div>
                            <div className="form-group input-group mb-3">
                                <input
                                    type="text"
                                    className="form-control"
                                    name="first_name"
                                    value={this.state.first_name}
                                    onChange={this.handleInputChange}
                                    placeholder="Your first name"
                                    maxLength="30"
                                    required
                                />
                                <input
                                    type="text"
                                    className="form-control"
                                    name="last_name"
                                    value={this.state.last_name}
                                    onChange={this.handleInputChange}
                                    placeholder="Your last name"
                                    maxLength="150"
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <input
                                    type="email"
                                    className="form-control"
                                    name="email"
                                    value={this.state.email}
                                    onChange={this.handleInputChange}
                                    placeholder="Your email id"
                                    required
                                />
                            </div>
                            <div className="form-group">
                                <div className="input-group mb-3 date" id="calendar" data-date-format="yyyy-mm-dd" data-date-end-date="0d">
                                    <input
                                        type="text"
                                        className="form-control"
                                        name="birthday"
                                        value={this.state.birthday}
                                        onChange={this.handleInputChange}
                                        placeholder="Your birth date"
                                        required
                                        readOnly
                                    />
                                    <div className="input-group-append">
                                        <div className="input-group-text">
                                            <span className="fa fa-calendar" aria-hidden="true"></span>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div className="form-group">
                                <div className="input-group mb-3">
                                    <input
                                        type={this.state.show_password ? 'text' : 'password'}
                                        className="form-control"
                                        name="password"
                                        value={this.state.password}
                                        onChange={this.handleInputChange}
                                        placeholder="Enter password"
                                        minLength="8"
                                        required
                                    />
                                    <div className="input-group-append">
                                        <div className="input-group-text" onClick={this.togglePasswordVisibility}>
                                            <span
                                                className={this.state.show_password ? 'fa fa-eye-slash' : 'fa fa-eye'}
                                                aria-hidden="true"
                                            ></span>
                                        </div>
                                    </div>
                                </div>
                                <ul className="helptext">
                                    <li className="non-selectable-text">Your password can't be too similar to other info.</li>
                                    <li className="non-selectable-text">Password must contain atleast 8 characters.</li>
                                    <li className="non-selectable-text">Don't put a commonly used word as password.</li>
                                    <li className="non-selectable-text">Password can't be entirely numeric.</li>
                                </ul>
                            </div>
                            <input
                                type="hidden"
                                id="id_timezone"
                                name="timezone"
                                value={this.state.timezone}
                                onChange={this.handleInputChange}
                            />
                            <input
                                type="submit"
                                className="btn btn-success"
                                value="Sign Up"
                            />
                        </form>
                        {error_show}
                    </div>
                </div>
            </div>
        );
    }
}

class SignInPageWithoutRouter extends React.Component {

    constructor(props) {
        super(props);
        this.state = {
            username: '',
            password: '',
            email: '',
            form_errors: [],
            show_password: false,
        };

        this.handleInputChange = this.handleInputChange.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.togglePasswordVisibility = this.togglePasswordVisibility.bind(this);
    }

    handleInputChange(event) {
        const target = event.target;
        const value = target.value;
        const name = target.name;

        this.setState({
            [name]: value,
        });
    }

    handleSubmit(event) {
        event.preventDefault();

        const state = this.state;
        var errors = [];

        if(state.username === '' || state.password === '' || state.email === '')
        {
            errors.append('Missing credential(s).');
        }
        else
        {
            if(!email_regex.test(state.email))
            {
                errors.append("This mail id can't be valid.");
            }
        }

        if(errors.length !== 0)
        {
            this.setState({
                form_errors: errors,
            });
        }
        else
        {
            fetch('http://127.0.0.1:8000/api/auth/signin/', {
                method: 'POST',
                headers: new Headers({
                    'content-type': 'application/json',
                }),
                cache: 'no-cache',
                mode: 'cors',
                body: JSON.stringify({
                    username: state.username,
                    password: state.password,
                    email: state.email,
                }),
            }).then((response) => {
                if(response.ok)
                {
                    response.json().then((data) => {
                        localStorage.setItem('authToken', data.token);
                        this.props.onLogin(data.user.id, data.user.first_name);
                        this.props.history.push('/');
                    });
                }
                else
                {
                    response.json().then((data) => {
                        let errors_from_server = [];

                        for(let key in data)
                        {
                            if(data.hasOwnProperty(key))
                            {
                                errors_from_server.concat(data[key]);
                            }
                        }

                        if(errors_from_server.length === 0)
                        {
                            errors_from_server.concat(['Unknown server error.',]);
                        }

                        this.setState({
                            form_errors: errors_from_server,
                        });
                    });
                }
            }, (error) => {
                this.setState({
                    form_errors: ['Network error.',],
                });
            });
        }
    }

    togglePasswordVisibility() {
        this.setState({
            show_password: !this.state.show_password,
        });
    }

    render() {
        const error_texts_li = this.state.form_errors.map((error, index) => {
            return <li key={index} className="error non-selectable-text">{error}</li>;
        });
        const error_show = (error_texts_li.length === 0) ? null : <div className="alert alert-warning"><ul>{error_texts_li}</ul></div>;

        return (
            <div className="container-fluid signin-super">
                <div className="row root-container signin-page-container">
                    <div className="for-background"></div>
                    <div className="col-md-8 col-lg-8 offset-xs-2 offset-sm-2 offset-md-2 offset-lg-2 greet-div">
                        <h1 className="great-header signup-header non-selectable-text mb-3">Sign In</h1>
                        <form onSubmit={this.handleSubmit}>
                            <div className="form-group">
                                <input
                                    type="text"
                                    className="form-control"
                                    name="username"
                                    value={this.state.username}
                                    onChange={this.handleInputChange}
                                    placeholder="Your username"
                                    autoFocus
                                    required
                                />
                            </div>
                            <div className="form-group input-group mb-3">
                                <input
                                    type={this.state.show_password ? 'text' : 'password'}
                                    className="form-control"
                                    name="password"
                                    value={this.state.password}
                                    onChange={this.handleInputChange}
                                    placeholder="Your password"
                                    required
                                />
                                <div className="input-group-append">
                                    <div className="input-group-text" onClick={this.togglePasswordVisibility}>
                                        <span
                                            className={this.state.show_password ? 'fa fa-eye-slash' : 'fa fa-eye'}
                                            aria-hidden="true"
                                        ></span>
                                    </div>
                                </div>
                            </div>
                            <div className="form-group">
                                <input
                                    type="email"
                                    className="form-control"
                                    name="email"
                                    value={this.state.email_id}
                                    onChange={this.handleInputChange}
                                    placeholder="Your email id"
                                    required
                                />
                            </div>
                            <input
                                type="submit"
                                className="btn btn-success"
                                value="Sign In"
                            />
                        </form>
                        {error_show}
                    </div>
                </div>
            </div>
        );
    }
}


export const SignInPage = withRouter(SignInPageWithoutRouter);
export const SignUpPage = withRouter(SignUpPageWithoutRouter);