"use strict";
var url_string = "/gallery_form"
$(document).ready(function(){
    if ($("#alert-message").val() != "") {
        alert($("#alert-message").val());
    }
});

async function get_links(user_id) {
    $.get("/links_table/" + user_id + "/", function(data, status){
        $("#links").html(data)
        $("[id^=btn-edit]").click(function(){
                load_link_form($(this).attr("link-id"));
            });
    });
}

function load_gallery_form() {
    $("#div-add-gallery").show();
    $("#btn-add-gallery").hide();
    $.get(url_gallery_form, function(data, status){
        $("#div-add-gallery").html(data);
        $("#btn-gallery-form").html("Add");
        $("#gallery-form").submit(post_gallery_form);
        $("#id_is_mature").change(mature);
        if(gallery_id) {
            $("#btn-gallery-form").html("Update");
            mature();
        }
    });
}

async function load_link_form(link) {
    console.log(link)
    let ustring = url_links_form;
    if (link != "") {
        ustring = ustring + link + "/";
    }
    console.log(ustring)
    $.get(ustring, function(data, status){
        $("#link-form-div").html(data)
    });
}

function mature() {
    if ($("#id_is_mature").prop('checked')) {
        $("#id_is_mature").prop('checked', true);
//        $("#id_is_public").prop('checked', false);
//        $("#id_is_public").attr("disabled", true);
        $("#id_public_date").attr("disabled", true);
    }
    else {
        $("#id_public_date").attr("disabled", false);
//        $("#id_is_public").attr("disabled", false);
    }
}

async function post_link() {
    console.log('post_link');
    let ustring = url_links_form;
    if ($("#id_id").val() != "") {
        ustring = ustring + $("#id_id").val() + "/";
    }
    let data = await $.post(ustring, {
        csrfmiddlewaretoken: $('#link-form > [name="csrfmiddlewaretoken"]').val(),
        'category': $("#id_category").val(),
        'url': $("#id_url").val()
    }).done(function( data ) {
        console.log(data);
        return data;
    }, "json");
    get_links(data['user']); // update links table
    load_link_form(""); // load empty form
}

async function post_gallery_form(e, gallery_id) {
    e.preventDefault();
    let data = await $.post(url_gallery_form, {
        csrfmiddlewaretoken: $('[name="csrfmiddlewaretoken"]').val(),
        'name': $("#id_name").val(),
        'description': $("#id_description").val(),
        'shoot_date': $("#id_shoot_date").val(),
        'is_mature': $("#id_is_mature").prop('checked'),
        'privacy_level': $("#id_privacy_level").val(),
        'public_date': $("#id_public_date").val(),
        'display_image': $("#id_display_image").val(),
        'release': $("#id_release").val(),
        'photographer': $("#id_photographer").val(),
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
        $("#btn-gallery-edit").show();
        return data;
    }, "json");
}
