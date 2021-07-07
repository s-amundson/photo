"use strict";
var url_string = "gallery_form"
$(document).ready(function(){
    $("#div-add-gallery").hide();
    $("#btn-add-gallery").click(function(){
        load_gallery_form();
    });
});

function load_gallery_form(gallery_id) {
    console.log(gallery_id);
    $("#div-add-gallery").show();
    $("#btn-add-gallery").hide()
    var url_string = "gallery_form"
    if(gallery_id) {
        url_string = "gallery_form/" + gallery_id + "/"
//        $("#student-row-" + student_id).hide()
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
    });
}

async function post_gallery_form(e) {
    e.preventDefault();
    let data = await $.post(url_string, {
            csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val(),
            'name': $("#id_name").val(),
            'shoot_date': $("#id_shoot_date").val(),
            'is_mature': $("#id_is_mature").prop('checked'),
            'is_public': $("#id_is_public").prop('checked'),
            'public_date': $("#id_public_date").val(),
        }).done(function( data ) {
        console.log(data);

        if ($("#no-gallery").length) {
            $("#no-gallery").remove();
        }
        let h = '<div class="row"><div class="col"><a href="' + data['url'] + '">' + $("#id_name").val() + '</a></div></div>'
        console.log(h)
        $("#gallery-list").append(h);
        $("#div-add-gallery").hide();
        $("#btn-add-gallery").show();
        return data;
    }, "json");
}