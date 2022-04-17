"use strict";
$(document).ready(function() {
    $("#image-form").submit(post_image);
    $("#btn-gallery-edit").click(function () {
        $(this).hide();
        load_gallery_form();
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
    h = h + data['filename'] + '</a><br/>' + data['privacy_level'].charAt(0).toUpperCase() + data['privacy_level'].slice(1) + '</div>';

    $("#images-div").append(h);
}

async function post_image(event) {
    event.preventDefault();
    $("#btn-image").prop("disabled",true)

    var form_data = new FormData($("#image-form")[0]);
    console.log(form_data);
    form_data.append('gallery', $("#id_gallery").val());
    form_data.append('privacy_level', $("#id_privacy_level").val())
    console.log(form_data);

    await $.ajax({
        url: url_image_upload, // point to server-side controller method
        dataType: 'json', // what to expect back from the server
        cache: false,
        contentType: false,
        processData: false,
        data: form_data,
        type: 'post',
        success: function (response) {
            console.log(response)
            add_image(response)
        },
        error: function (response) {
            alert(response); // display error response from the server
        }
    });
    $("#btn-image").prop("disabled",false)
}