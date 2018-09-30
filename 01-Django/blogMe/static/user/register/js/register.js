$(function(){

    $('#submit_first').click(function(){
        //remove classes
        $('#first_step input').removeClass('error').removeClass('valid');

        //ckeck if inputs aren't empty
        var fields = $('#first_step input[type=text], #first_step input[type=password]');
        var error = 0;
        fields.each(function(){
            var name = $(this).val();
            if( name.length<4 || name==field_values[$(this).attr('id')] ) {
                $(this).addClass('error');
                error++;
            } else {
                $(this).addClass('valid');
            }
        });
        if(!error) {
            if( $('#password').val() != $('#cpassword').val() ) {
                    $('#first_step input[type=password]').each(function(){
                        $(this).removeClass('valid').addClass('error');
                    });
                    return false;
            } else {   
                //update progress bar
                $('#progress_text').html('33% Complete');
                $('#progress').css('width','113px');
            }               
        } else return false;
    });

    $('#submit_fourth').click(function(){
        //send information to server
        alert('Data sent');
    });

});