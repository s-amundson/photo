"use strict";
$(document).ready(function() {
    $("#btn-gallery-edit").click(function () {
        $(this).hide();
        load_gallery_form();
    });
    $("#btn-image-privacy").click(function() {
        console.log($("#div_image_privacy").is(":visible"))
        if ($("#div_image_privacy").is(":visible")) {
            $(this).html("Show Privacy Info");
            $("#div_image_privacy").hide();
        }
        else {
            $(this).html("Hide Privacy Info");
            $("#div_image_privacy").show();
        }
    });
    $("#div_image_privacy").hide();
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
