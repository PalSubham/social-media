function resize_image_brief()
{
    $('.all-image').each(function (index, object) {
        let images = $(this).children('img');
        let size = images.length;

        for(let i = 0; i < size; i++)
        {
            if(images[i].naturalWidth <= images[i].naturalHeight)
            {
                $(images[i]).width('100%').height('auto');
            }
            else
            {
                $(images[i]).width('auto').height('100%');
            }
        }
        
        return;
    });
    console.log('hello');
    return;
}

$(window).ready(function () {
    
    resize_image_brief();
    
    return;
});

