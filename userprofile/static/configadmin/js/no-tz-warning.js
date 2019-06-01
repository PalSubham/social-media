window.onload = function () {
    function tzOffset()
    {
        let d = new Date();
        let n = d.getTimezoneOffset();
        n *= -60;
        return n.toString();
    }

    document.getElementsByTagName('body')[0].setAttribute('data-admin-utc-offset', tzOffset());
    return;
}