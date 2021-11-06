$(document).ready(function(){
    $('#course_level').prop('disabled',true);
    $("#course_level option").each(function(){$(this).hide();});
    $('#course_mod').prop('disabled',true);
    $("#course_mod option").each(function(){$(this).hide();});
  	$('#post_type').change(function(){
        if($('#post_type').val() == 'curso'){
            $('#course_level').prop('disabled',true);
            $("#course_level option").each(function(){$(this).hide();});
            $('#job_level').prop('disabled', false);
            $("#job_level option").each(function(){$(this).show();});
            $('#course_mod').prop('disabled',true);
            $("#course_mod option").each(function(){$(this).hide();});
            $('#job_mod').prop('disabled', false);
            $("#job_mod option").each(function(){$(this).show();});
        }
        else{
            $('#job_level').prop('disabled',true);
            $("#job_level option").each(function(){$(this).hide();});
            $('#course_level').prop('disabled', false);
            $("#course_level option").each(function(){$(this).show();});
            $('#job_mod').prop('disabled',true);
            $("#job_mod option").each(function(){$(this).hide();});
            $('#course_mod').prop('disabled', false);
            $("#course_mod option").each(function(){$(this).show();});
        }
    });
});