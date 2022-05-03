"use strict";
var template_choice = "#temp_template_choice";
var url = ''
$(document).ready(function() {

    if (document.URL.split('/').indexOf('model_release') > 0) {
        template_choice = "#id_template";
        console.log($(template_choice).val())
        url = document.URL.substring(0, document.URL.indexOf('model'))
//        $('label[for="' + $("#id_file").attr("id") + '"]').hide();
        get_template();
        $("#model-release *").filter(':input').each(function(){
            $(this).change(post_template);
        });
//        $('#id_template').parents('p').hide();
    }
    else {
        $("#id_template").prop('disabled', true);
        get_template();
        $("#template-form-div").hide();
    //    $("#use-template-div").hide();
        $("#btn-add-template").click(add_template);
        $("#temp_template_choice").change(get_template);

        $("#model-release *").filter(':input').each(function(){
            $(this).change(post_template);
        });
    }
    $("#model-release").submit(function (event) {
        event.preventDefault();
        $("#id_template").prop('disabled', false);
        if (!sig.signature('isEmpty')) {
            console.log('submit')
            $(".signature").val(sig.signature('toDataURL', 'image/jpeg', 0.8));
//            $(this).unbind();
//            $(this).submit();
        }
        $(this).off("submit");
        $(this).submit();
    });
    console.log(template_choice)
    var sig = $('#sig').signature();

    $("#btn-submit").prop('disabled', signature_required);
    sig.signature({
    change: function(event, ui) {
        if (sig.signature('isEmpty')) {
            console.log('sig empty');
            $("#btn-submit").prop('disabled', true);
        }
        else {
            $("#btn-submit").prop('disabled', false);
        }
    }});
	$('#clear').click(function(e) {
	    e.preventDefault();
		sig.signature('clear');
	});
	$('#json').click(function() {
		alert(sig.signature('toJSON'));
	});
	$('#svg').click(function() {
		alert(sig.signature('toSVG'));
	});
	$("#sign_in_form").submit(function(e) {
	    e.preventDefault();
    });
});

function add_template() {
    $("#template-form-div").show();
}

function get_template() {
//  Get the selected release template from the server
    if (form_instance) {
        console.log(url_template)
        $.get(url_template, function(data, status){
            $("#template-view").html(data);

        });
        if (template_choice == "#temp_template_choice"){
            $("#id_template").val($("#temp_template_choice").val());
        }
    }
}
async function post_template(event) {
    await $.post(url_release_update, $("#model-release").serializeArray(), function(data, status){
        if (data['status'] == 'success') {
            get_template();
        }
    });
    }
//async function post_template(event) {
//    console.log('release_preview/' + $(template_choice).val() + '/')
//    await $.post(url + 'release_preview/' + $(template_choice).val() + '/', {
//        csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val(),
//        'description': $("#model-release > p:nth-child(2) > textarea:nth-child(2)").val(),
//        'name': $("#name").val(),
//        'photo_model': $("#id_photo_model").val(),
//        'shoot_date' : $("#id_shoot_date").val(),
//        'template': $("#id_template").val(),
//        'compensation': $("#id_compensation").val(),
//        'is_mature': $("#id_is_mature").prop('checked'),
//        'use_first_name': $("#id_use_first_name").prop('checked'),
//        'use_full_name': $("#id_use_full_name").prop('checked'),
//        'use_nickname': $("#id_use_nickname").prop('checked')
//    }, function(data, status){
//        $("#template-view").html(data);
//        return data;
//    }, "html");
//}