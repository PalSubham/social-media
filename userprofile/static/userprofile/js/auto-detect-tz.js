$(window).ready(function (){
    if(Intl && (tz = Intl.DateTimeFormat().resolvedOptions().timeZone))
    {
        $('#id_timezone').val(tz.toString());
    }

    return;
});