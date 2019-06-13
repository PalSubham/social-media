$(window).ready(function () {
    $('.all-avatar img').each(function (index, object) {
        if($(this).naturalWidth <= $(this).naturalHeight)
        {
            $(this).width('100%').height('auto');
        }
        else{
            $(this).width('auto').height('100%');
        }
        return;
    });
    return;
});