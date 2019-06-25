/*
Shows & hides reaction dropdown.
Shows & hides comment form.
*/

$(window).ready(function () {

    $(window).click(function (event) {
        if(/^\/details\/[0-9]*\/$/.test(window.location.pathname.toString()))
        {
            if(!(event.target.matches('#dropdown') || event.target.matches('#detail-react-image')) && $('#dropdown-content').is('.detail-dropdown-content-show'))
            {
                $('#dropdown-content').removeClass('detail-dropdown-content-show');
            }
        }
        return;
    });

    return;
});

function showReactionDropdown()
{
    $('#dropdown-content').toggleClass('detail-dropdown-content-show');
    return;
}

function showCommentForm()
{
    if($('.all-cover').is('.hide-comment-form'))
    {
        $('.all-cover').removeClass('hide-comment-form');
        $('body').css('overflow', 'hidden');
        $('#comment-form textarea').focus();
    }
    return;
}

function hideCommentForm()
{
    if(!$('.all-cover').is('.hide-comment-form'))
    {
        $('.all-cover').addClass('hide-comment-form');
        $('body').css('overflow', 'auto');
        $('#comment-form').trigger('reset');
        unselectCommentImage();
    }
    return;
}
