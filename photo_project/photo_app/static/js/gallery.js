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
    $(".carousel-btn").click(function() {
        console.log($(this).attr("img_id"))
        post_carousel($(this))
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

async function post_carousel(element) {
    let c = element.attr("carousel")
    if (c == "True") {
        console.log("set false")
        c = "False"
        }
    else {
        console.log("set True")
        c = "True"
    }
    let data = await $.post(url_image_carousel + element.attr("img_id") + "/", {
            csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val(),
            carousel: c,
        }
    ).done(function( data ) {
        console.log(data);
        if(data['carousel']) {
            element.html("Remove from Carousel");
            element.attr("carousel", "True")
        } else {
            element.html("Add to Carousel");
            element.attr("carousel", "False")
        }
    });
}