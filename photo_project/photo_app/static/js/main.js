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

function load_gallery_form(gallery_id) {
    $("#div-add-gallery").show();
    $("#btn-add-gallery").hide();
    if(gallery_id) {
        url_string = "/gallery_form/" + gallery_id + "/";
    }
    $.get(url_string, function(data, status){
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
    let ustring = '/links_form';
    if (link != "") {
        ustring = ustring + "/" + link + "/";
    }
    $.get(ustring, function(data, status){
        $("#link-form-div").html(data)
    });
}

function mature() {
    console.log('update mature')
    if ($("#id_is_mature").prop('checked')) {
        $("#id_is_mature").prop('checked', true);
        $("#id_is_public").prop('checked', false);
        $("#id_is_public").attr("disabled", true);
        $("#id_public_date").attr("disabled", true);
    }
    else {
        $("#id_public_date").attr("disabled", false);
        $("#id_is_public").attr("disabled", false);
    }
}

async function post_link() {
    console.log('post_link');
    let ustring = '/links_form';
    if ($("#id_id").val() != "") {
        ustring = ustring + "/" + $("#id_id").val() + "/";
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
