function sendReaction(event)
{
    var target = (event.target) ? event.target : event.srcElement;
    var emoji_number = $(target).attr('emoji');
    var post_id = $(target).attr('post');
    console.log(target);

    $.ajax({
        type: 'GET',
        url: '/reaction/',
        data: {'post_id': post_id, 'reaction_number': emoji_number},
        dataType: 'json',
        success: function(data, textStatus, jqXHR) {

            if(data.success)
            {
                $('.post-brief-reaction-no').text(data.reactions + ' reaction' + data.plural);
                $('#detail-react-image').attr('src', '/static/post/svg/r' + emoji_number + '.svg');
            }
            return;
        }
    });
}