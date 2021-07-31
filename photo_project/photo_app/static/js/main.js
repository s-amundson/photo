"use strict";
var url_string = "/gallery_form"
$(document).ready(function(){
    if ($("#alert-message").val() != "") {
        alert($("#alert-message").val());
    }
});

function load_gallery_form(gallery_id) {
    console.log(gallery_id);
    $("#div-add-gallery").show();
    $("#btn-add-gallery").hide();
    if(gallery_id) {
        url_string = "/gallery_form/" + gallery_id + "/";
    }
    console.log('load form')
    console.log(url_string)
    $.get(url_string, function(data, status){
        $("#div-add-gallery").html(data);
        $("#btn-gallery-form").html("Add");
        $("#gallery-form").submit(post_gallery_form);
        $("#id_is_mature").change(function() {
            if (this.checked) {
                $("#id_is_public").prop('checked', false);
                $("#id_is_public").attr("disabled", true);
                $("#id_public_date").attr("disabled", true);
            }
            else {
                $("#id_public_date").attr("disabled", false);
            }
        });
        if(gallery_id) {
            $("#btn-gallery-form").html("Edit")
        }
    });
}

async function post_gallery_form(e, gallery_id) {
    e.preventDefault();
    var url_string = "/gallery_form"
    if($("#id_gallery").val()) {
        url_string = "/gallery_form/" + $("#id_gallery").val() + "/";
    }
    let data = await $.post(url_string, {
        csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val(),
        'name': $("#id_name").val(),
        'shoot_date': $("#id_shoot_date").val(),
        'is_mature': $("#id_is_mature").prop('checked'),
        'is_public': $("#id_is_public").prop('checked'),
        'public_date': $("#id_public_date").val(),
        'display_image': $("#id_display_image").val(),
    }).done(function( data ) {
        console.log(data);

        if ($("#no-gallery").length) {
            $("#no-gallery").remove();
        }
        let h = '<div class="col border mx-auto"><a href="' + data['url'] + '">' + $("#id_name").val() + '</a></div>'
        console.log(h)
        $("#gallery-list").append(h);
        $("#div-add-gallery").hide();
        $("#btn-add-gallery").show();
        return data;
    }, "json");
}
