import React from 'react';
import './index.css';


function LoadingHome(props) {
    const message = (props.Error === '') ? 'loading...' : props.Error;
    const errButton = (props.Error !== '') ? <button onClick={props.onErrorButtonFunc}>Try again...</button> : null;

    return (
        <div className="w-100 h-100 m-0 p-0">
            <div id="test-text">{message}</div>
            {errButton}
        </div>
    );
}

function UnAuthHome (props) {

    return (
        <div>signed out...</div>
    );

}

class AuthHome extends React.Component {

    render() {
        return (
            <div>signed in...</div>
        );
    }

}


export { LoadingHome, UnAuthHome, AuthHome };