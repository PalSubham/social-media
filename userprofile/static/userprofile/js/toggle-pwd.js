$(window).ready(function (){
    $('#toggle-pwd-signin').on('click', function (event) {
        if($(this).hasClass('fa-eye'))
        {
            $(this).addClass('fa-eye-slash');
            $(this).removeClass('fa-eye');
            $('#toggle-pwd-input-signin').attr('type', 'text');
            return;
        }
        else if($(this).hasClass('fa-eye-slash'))
        {
            $(this).addClass('fa-eye');
            $(this).removeClass('fa-eye-slash');
            $('#toggle-pwd-input-signin').attr('type', 'password');
            return;
        }
    });

    $('#toggle-pwd-signup').on('click', function (event) {
        if($(this).hasClass('fa-eye'))
        {
            $(this).addClass('fa-eye-slash');
            $(this).removeClass('fa-eye');
            $('#toggle-pwd-input1-signup').attr('type', 'text');
            $('#toggle-pwd-input2-signup').attr('type', 'text');
            return;
        }
        else if($(this).hasClass('fa-eye-slash'))
        {
            $(this).addClass('fa-eye');
            $(this).removeClass('fa-eye-slash');
            $('#toggle-pwd-input1-signup').attr('type', 'password');
            $('#toggle-pwd-input2-signup').attr('type', 'password');
            return;
        }
    });
});