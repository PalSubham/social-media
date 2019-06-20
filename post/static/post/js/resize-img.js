$(window).ready(function () {
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
    
    return;
});