
$(document).ready(function(){

$('form[name=signup_form').submit(function (e){
    var $form=$(this);
    var $error=$form.find('.error');
    var data=$form.serialize();
    e.preventDefault();
    $('#loader').show();
    $('#signupform').hide();



    $.ajax({

        url:"/users/signup",
        type:"POST",
        data: data,
        dataType:"json",
        success:function(resp){
                console.log('hi');
                window.location.href='/Home/';
        },
        error:function(resp){
            $('#loader').hide();
            $('#signupform').show();

            $error.text(resp.responseJSON.error).removeClass('error--hidden');
            

        }


    });

});
});


