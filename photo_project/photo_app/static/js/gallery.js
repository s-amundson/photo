"use strict";
$(document).ready(function() {
    $("#image-form").submit(post_image);
    $("#btn-gallery-edit").click(function () {
        $(this).hide();
        load_gallery_form($("#id_gallery").val());
    });
});

function add_image(data) {
    if ($("#no-image").length) {
        $("#no-image").remove()
    }
    console.log(data["image"])
    let h = '<div class="col border mx-auto">';
    h = h + '<a target="_blank" href="' + $("#id_image_base_url").val() + "/" + data['id'] + '">';
    h = h + '<img width="' + data['thumb_width'] + 'px" src="' + $("#id_thumb_base_url").val() + "/" + data['id']  + '"><br/>';
    h = h + data['filename'] + '</a></div>';

    $("#images-div").append(h);
}

async function post_image(event) {
    event.preventDefault();
    $("#btn-image").prop("disabled",true)

//    var file_data = $('#id_image').prop('files')[0];
    var form_data = new FormData($("#image-form")[0]);
    console.log(form_data);
//    form_data.append('image', file_data);
//    form_data.append('csrfmiddlewaretoken', $('[name="csrfmiddlewaretoken"]').val());
    form_data.append('gallery', $("#id_gallery").val());
    console.log(form_data);

    await $.ajax({
        url: "/image_upload/" + $("#id_gallery").val() + "/", // point to server-side controller method
        dataType: 'json', // what to expect back from the server
        cache: false,
        contentType: false,
        processData: false,
        data: form_data,
        type: 'post',
        success: function (response) {
//            $('#msg').html(response); // display success response from the server
            console.log(response)
            add_image(response)
        },
        error: function (response) {
            alert(response); // display error response from the server
        }
    });
    $("#btn-image").prop("disabled",false)
}