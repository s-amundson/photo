"use strict";
$(document).ready(function() {
    $("#image-form").submit(post_image);

});
function add_image(data) {
    if ($("#no-image").length) {
        $("#no-image").remove()
    }
    console.log(data["image"])
    let h = '<div class="col border mx-auto">';
    h = h + '<a target="_blank" href="' + data['image'] + '">';
    h = h + '<img width="' + data['thumb_width'] + 'px" src="' + data['image'] + '"><br/>';
    h = h + data['width'] + ' x ' + data['height'] + '</a></div>';

    $("#images-div").append(h);
}

function post_image(event) {
    event.preventDefault();
    var file_data = $('#id_image').prop('files')[0];
    var form_data = new FormData($("#image-form")[0]);
    console.log(form_data);
//    form_data.append('image', file_data);
//    form_data.append('csrfmiddlewaretoken', $('[name="csrfmiddlewaretoken"]').val());
    form_data.append('gallery', $("#id_gallery").val());
    console.log(form_data);

    $.ajax({
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
}