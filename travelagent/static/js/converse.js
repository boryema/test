$(document).ready(function(){
    $('#send').attr('disabled', 'disabled');
    $('#converse').keyup(function(){
        if($(this).val()!= 0){
        $('#send').removeAttr('disabled');
        }
        else{
        $('#send').attr('disabled','disabled')
        }

    });
});







