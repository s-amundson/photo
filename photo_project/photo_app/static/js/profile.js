"use strict";
$(document).ready(function() {
    get_profile_info()
    $("#btn-address-edit").click(function () {
        $("#profile-address").hide();
        $("#profile-form-div").show();
    });
});

async function get_profile_info() {
    await $.get("profile_info_api", function(data, status){
        console.log(data);
        $("#id_first_name").val(data['first_name']);
        $("#id_last_name").val(data['last_name']);
        $("#id_street").val(data['street']);
        $("#id_city").val(data['city']);
        $("#id_state").val(data['state']);
        $("#id_post_code").val(data['post_code']);
        $("#id_phone").val(data['phone']);
        $("#id_dob").val(data['dob']);
        $("#id_is_model").prop('checked', data['is_model']);
        $("#id_nickname").val(data['nickname']);

        if (data['first_name'] == "") {
            $("#profile-address").hide();
            $("#profile-form-div").show();
            $("#profile-form").submit(function(e){
                e.preventDefault();
                post_address_function($("#btn-address-edit").attr("model_id") == "");
            });
        }
        else {
            $("#profile-form-div").hide();
            $("#profile-address").show();
        }
    });
}

async function post_address_function(model_id) {
    let data = await $.post("profile_info_api", {
        csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val(),
        'first_name': $("#id_first_name").val(),
        'last_name': $("#id_last_name").val(),
        'street': $("#id_street").val(),
        'city' : $("#id_city").val(),
        'state': $("#id_state").val(),
        'post_code': $("#id_post_code").val(),
        'phone': $("#id_phone").val(),
        'dob': $("#id_dob").val(),
        'is_model': $("#id_is_model").prop('checked'),
        'nickname': $("#id_nickname").val()
    }, function(data, status){
        console.log(data)
        return data;
    }, "json");
    $("#model-name").html($("#id_first_name").val() + " " + $("#id_last_name").val())
    $("#address1").html($("#id_street").val());
    $("#address2").html($("#id_city").val() + " " + $("#id_state").val() + " " + $("#id_post_code").val())
    $("#phone").html($("#id_phone").val())

    $("#profile-address").show();
    $("#profile-form-div").hide();
}