const resizeBriefImage = () => {
    window.$('.all-image').each(function (index, object) {
        const images = $(this).children('img');
        const size = images.length;

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
    });
};

export default resizeBriefImage;