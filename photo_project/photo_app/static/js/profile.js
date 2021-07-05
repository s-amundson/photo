"use strict";
$(document).ready(function() {
    if ($("#btn-address-edit").attr("model_id") == "") {
        $("#photo-model-address").hide();
        $("#photo-model-form").show();
//        load_address_form($("#btn-address-edit").attr("model_id"));
        $("#model-form").submit(function(e){
            e.preventDefault();
            post_model_function($("#btn-address-edit").attr("model_id") == "");
        });
    }
});

//function load_address_form(model_id) {
//    console.log(model_id);
//    $("#photo-model-address").hide();
//
//    $.get("model_info", function(data, status){
//        $("#photo-model-form").html(data);
//        $("#photo-model-form").show();
//
//        $("#model-form").submit(function(e){
//            e.preventDefault();
//            post_model_function(model_id)
//        });
//
//    });
//}

async function post_model_function(model_id) {
    console.log('on submit')
    let url_string = "model_info_api";
    if (model_id != "") {
        url_string = url_string + "/" + family_id + "/";
    }
    let data = await $.post(url_string, {
        csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val(),
        'first_name': $("#id_first_name").val(),
        'last_name': $("#id_last_name").val(),
        'street': $("#id_street").val(),
        'city' : $("#id_city").val(),
        'state': $("#id_state").val(),
        'post_code': $("#id_post_code").val(),
        'phone': $("#id_phone").val(),
        'dob': $("#id_dob").val()
    }, function(data, status){
        console.log(data)
        return data;
    }, "json");
    $("#model-name").html($("#id_first_name").val() + " " + $("#id_last_name").val())
    $("#address1").html($("#id_street").val());
    $("#address2").html($("#id_city").val() + " " + $("#id_state").val() + " " + $("#id_post_code").val())
    $("#phone").html($("#id_phone").val())

    $("#photo-model-address").show();
    $("#photo-model-form").hide();
}