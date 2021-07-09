"use strict";
$(document).ready(function() {
    $("#id_template").prop('disabled', true);
    get_template();
    $("#template-form-div").hide();
//    $("#use-template-div").hide();
    $("#btn-add-template").click(add_template)
    $("#id_template_choice").change(get_template)
});

function add_template() {
    $("#template-form-div").show();
}

function get_template() {
//  Get the selected release template from the server
    $.get('release_preview/' + $("#id_template_choice").val() + '/', function(data, status){
        $("#template-view").html(data);
    });
    $("#id_template").val($("#id_template_choice").val())
}

//function post_template(event) {
//    event.preventDefault();
//    var form_data = new FormData($("#template-form")[0]);
////    form_data.append('gallery', $("#id_gallery").val());
//    console.log(form_data);
//    $.ajax({
//        url: "/image_upload/" + $("#id_gallery").val() + "/", // point to server-side controller method
//        dataType: 'json', // what to expect back from the server
//        cache: false,
//        contentType: false,
//        processData: false,
//        data: form_data,
//        type: 'post',
//        success: function (response) {
////            $('#msg').html(response); // display success response from the server
//            console.log(response)
//            add_image(response)
//        },
//        error: function (response) {
//            alert(response); // display error response from the server
//        }
//    });
//}