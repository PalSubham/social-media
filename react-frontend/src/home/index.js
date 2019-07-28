import React from 'react';
import { Link } from 'react-router-dom';
import write_share from './media/write-share.svg';
import image_share from './media/image-share.svg';
import r2 from './media/r2.svg';
import r3 from './media/r3.svg';
import r4 from './media/r4.svg';
import r5 from './media/r5.svg';
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
        <div className="m-0 p-0 w-100 h-100">
            <div className="container">
                <div className="row root-container">
                    <div className="for-background"></div>
                    <div className="col-md-10 col-lg-10 offset-xs-1 offset-sm-1 offset-md-1 offset-lg-1 greet-div">
                        <h1 className="great-header non-selectable-text">sharELand</h1>
                        <div id="talk" className="non-selectable-text">
                            Hello there,<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Here is a new social media app for you. You can follow
                            your dears, share rhythms and colors of your mind, react to a post as heart says and give your
                            precious comments and replies.<br />&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Give it a try and you will never regret.
                            Have fun!!!
                        </div>
                    </div>
                </div>
            </div>

            <div className="container-fluid signup-container">
                <div className="row">
                    <div className="col-md-8 col-lg-8 d-flex align-items-center justify-content-center signup">
                        <p className="non-selectable-text">No account yet?<br />Create your account now</p>
                    </div>
                    <div className="col-md-4 col-lg-4 d-flex align-items-center justify-content-center signup">
                        <Link to="/signup/"><button type="Button" className="btn btn-outline-dark btn-lg">Sign Up</button></Link>
                    </div>
                </div>
            </div>

            <div className="container-fluid" id="feature-talks">
                <div className="row feature-row1">
                    <div className="col-md-4 col-lg-4 d-flex align-items-center justify-content-center signup">
                        <img id="feature-image1" src={write_share} alt="" />
                    </div>
                    <div className="col-md-8 col-lg-8 d-flex align-items-center justify-content-center signup">
                        <p className="feature-talk feature-talk1 non-selectable-text">Share your thoughts!!!</p>
                    </div>
                </div>
                <div className="row feature-row2">
                    <div className="col-md-8 col-lg-8 d-flex align-items-center justify-content-center signup">
                        <p className="feature-talk feature-talk2 non-selectable-text">Share the colors of your heart!!!</p>
                    </div>
                    <div className="col-md-4 col-lg-4 d-flex align-items-center justify-content-center signup">
                        <img id="feature-image1" src={image_share} alt="" />
                    </div>
                </div>
                <div className="row feature-row3">
                    <div className="col-md-2 col-lg-2 d-flex align-items-center justify-content-center signup">
                        <img className="emoji-ex" src={r3} alt="" />
                    </div>
                    <div className="col-md-2 col-lg-2 d-flex align-items-center justify-content-center signup">
                        <img className="emoji-ex" src={r5} alt="" />
                    </div>
                    <div className="col-md-4 col-lg-4 d-flex align-items-center justify-content-center signup">
                        <p className="feature-talk feature-talk3 non-selectable-text">Reflect feelings through reactions!!!</p>
                    </div>
                    <div className="col-md-2 col-lg-2 d-flex align-items-center justify-content-center signup">
                        <img className="emoji-ex" src={r4} alt="" />
                    </div>
                    <div className="col-md-2 col-lg-2 d-flex align-items-center justify-content-center signup">
                        <img className="emoji-ex" src={r2} alt="" />
                    </div>
                </div>
            </div>

            <footer>
                <div className="container-fluid">
                    <div className="row my-3">
                        <div className="col-md-12 col-lg-12 d-flex align-items-center justify-content-center">
                            <h1 className="non-selectable-text">sharELand</h1>
                        </div>
                    </div>
                    <div className="row">
                        <div className="col-md-6 col-lg-6 d-flex align-items-center justify-content-center my-3">
                            <Link to="/signup/"><button type="Button" className="btn btn-light btn-lg">Sign Up</button></Link>
                        </div>
                        <div className="col-md-6 col-lg-6 d-flex align-items-center justify-content-center my-3">
                            <Link to="/signin/"><button type="Button" className="btn btn-light btn-lg">Sign In</button></Link>
                        </div>
                    </div>
                    <div className="row my-3">
                        <div className="col-md-12 col-lg-12 d-flex align-items-center justify-content-center">
                            <h3 className="non-selectable-text">Thank You</h3>
                        </div>
                    </div>
                </div>
            </footer>
        </div>
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