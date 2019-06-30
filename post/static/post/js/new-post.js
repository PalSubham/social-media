/*
All code related to the form for new post.
Activates and deactivates submit button.
Creates extra image input for at most 50 images.
Unselects an image.
*/

$(window).ready(function () {

    $('#post-form textarea').keyup(function () {
        let submit = $('#post-form input[type=submit]');

        if($(this).val().length == 0 && $('.single-image-container').length == 1)
        {
            submit.attr('disabled', 'disabled');
        }
        else
        {
            submit.removeAttr('disabled');
        }

        return;
    });

    return;
});

function new_image(serial_no)
{
    serial_no = serial_no.toString();

    let html = `
    <div class="single-image-container px-2 py-2 position-relative">
        <input class="form-control-file post-file-input" type="file" name="post_images" accept="image/*" id="file_${serial_no}" onchange="moreImage(event)">
        <label for="file_${serial_no}" class="h-100 w-100 position-relative" title="New Image">
            <img class="position-absolute m-auto w-auto h-auto" src=${add_post_img}>
        </label>
        <div class="remove-post-image rounded-circle position-absolute" title="Remove image" onclick="removeImage(event)"><span class="fa fa-remove"></span></div>
    </div>
    `;

    return html;
}

function moreImage(event)
{
    var element = event.currentTarget;
    var id = $(element).attr('id').replace(/^\D+/g, '');
    var submit = $('#post-form input[type=submit]');

    if(element.files.length != 0 && element.files[0])
    {
        $(element).siblings('label').removeAttr('for title').css('cursor', 'auto');
        $(element).removeAttr('onchange').css('pointer-events', 'none');
        $(element).siblings('div.remove-post-image').css('display', 'block');

        let reader = new FileReader();
        reader.onload = function (e) {
            $(element).siblings('label').children('img').attr('src', e.target.result);
            return;
        }
        reader.readAsDataURL(element.files[0]);

        $(element).parent().addClass('mr-2');
        
        if($('.post-file-input').length < 50)
        {
            $('#pad').before(new_image(parseInt(id) + 1));
        }
    }

    if($('#post-form textarea').val().length == 0 && $('.post-file-input').length == 1)
    {
        submit.attr('disabled', 'disabled');
    }
    else
    {
        submit.removeAttr('disabled');
    }

    return;
}

function removeImage(event)
{
    var submit = $('#post-form input[type=submit]');
    
    $(event.currentTarget).parent().remove();

    if($('#post-form textarea').val().length == 0 && $('.post-file-input').length == 1)
    {
        submit.attr('disabled', 'disabled');
    }
    else
    {
        submit.removeAttr('disabled');
    }

    return;
}