$(window).ready(function () {
    let url_part = window.location.pathname.toString();
    let reg = /^\/details\/[0-9]*\/$/;

    if(reg.test(url_part))
    {
        setInterval(function () {
            console.log('hello');
            return;
        }, 3000);
    }
    return;
});