/*
Saves reaction
Saves comment
Unselects comment image
*/

$(window).ready(function () {

    $('#comment-form textarea').keyup(function () {
        let empty = false;
        let submit = $('#comment-form input[type=submit]');

        if($(this).val().length == 0 && $('#comment-form input[type=file]')[0].files.length == 0)
        {
            empty = true;
        }

        if(empty)
        {
            submit.attr('disabled', 'disabled');
        }
        else
        {
            submit.removeAttr('disabled');
        }

        return;
    });

    $('#comment-form input[type=file]').change(function (event) {
        let empty = false;
        let submit = $('#comment-form input[type=submit]');
        

        if(event.target.files.length == 0)
        {
            if($('#comment-form textarea').val().length == 0)
            {
                empty = true;
            }
        }
        else
        {
            let filename = event.target.files[0].name;
            let mod_filename = (filename.length > 15) ? (filename.slice(0, 12) + '...') : filename;
            let label = $('label[for="comment-image-input"]');
            label.html('<span class="fa fa-upload"></span> ' + mod_filename);
            label.attr('title', filename);
        }

        if(empty)
        {
            submit.attr('disabled', 'disabled');
        }
        else
        {
            submit.removeAttr('disabled');
        }

        return;
    });

    $('#comment-form').submit(function (event) {
        event.preventDefault(); // Prevents the default form submission technique.

        var form = $(this);

        $.ajax({
            type: form.attr('method'),
            url: form.attr('action'),
            data: new FormData(this),
            enctype: 'multipart/form-data',
            contentType: false,
            processData: false,
            cache: false,
            beforeSend: function (jqXHR, settings) {

                if(!csrfSafeMethod(settings.method) && !settings.crossDomain)
                {
                    jqXHR.setRequestHeader('X-CSRFToken', csrftoken);
                }

                return;
            },
            success: function (data, textStatus, jqXHR) {
                if(data.success)
                {
                    setTimeout(function () {
                        $('#comment-close').trigger('click');
                        return;
                    }, 10);
                    
                    $('.post-brief-comment-no').text(data.comments + ' reaction' + data.plural);
                    $('#more-comments').append(data.new_comment_html);
                }
                else
                {
                    alert('Error...Please resubmit the comment');
                }
                return;
            },
            error: function (jqXHR, textStatus, errorThrown) {
                alert('Error...Please resubmit the comment');
                return;
            }
        });
    })
    return;
});

var csrftoken = Cookies.get('csrftoken'); // CSRF token from 'csrftoken' cookie in response header

function csrfSafeMethod(method)
{
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sendReaction(event)
{
    var target = (event.target) ? event.target : event.srcElement;
    var emoji_number = $(target).attr('emoji');
    var post_id = $(target).attr('post');

    $.ajax({
        type: 'POST',
        url: '/reaction/',
        data: {'post_id': post_id, 'reaction_number': emoji_number},
        dataType: 'json',
        cache: false,
        beforeSend: function (jqXHR, settings) {

            if(!csrfSafeMethod(settings.method) && !settings.crossDomain)
            {
                jqXHR.setRequestHeader('X-CSRFToken', csrftoken);
            }
            return;
        },
        success: function(data, textStatus, jqXHR) {

            if(data.success)
            {
                $('.post-brief-reaction-no').text(data.reactions + ' reaction' + data.plural);
                $('#detail-react-image').attr('src', '/static/post/svg/r' + emoji_number + '.svg');
            }
            else
            {
                alert('Error...Please try again');
            }
            return;
        },
        error: function (jqXHR, textStatus, errorThrown) {
                alert('Error...Please try again');
                return;
        }
    });

    return;
}

function unselectCommentImage()
{
    let input = $('#comment-image-input');
    let label = $('label[for="comment-image-input"]');
    input.val($(this).prop('defaultValue')).trigger('change');
    label.html('<span class="fa fa-upload"></span> Upload an image');
    label.removeAttr('title');
    return;
}

function loadMore(event, what)
{
    var loaded_comments = $('#loaded-comments');
    var id = $('#comment-form input[type=hidden]').val();
    var target = event.currentTarget;

    $.ajax({
        type: 'GET',
        url: '/extra/',
        data: {'what': what, 'post_id': id, 'loaded': loaded_comments.val()},
        dataType: 'json',
        cache: false,
        success: function (data, textStatus, jqXHR) {

            if(data.success)
            {
                var comment_container = $('#more-comments');
                loaded_comments.val(parseInt(loaded_comments.val()) + 3);

                if(loaded_comments.val() >= $('#total-comments').val())
                {
                    setTimeout(function () {
                        $(target).css('visibility', 'hidden');
                        return;
                    }, 10);
                    
                }

                for(let i = 0; i < data.extra_comments.length; i++)
                {
                    comment_container.prepend(data.extra_comments[i]);
                }

                resize_image_brief();
            }

            return;
        }
    });

    return;
}