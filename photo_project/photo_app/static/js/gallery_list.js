"use strict";
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
    });
    $("#gallery-form").submit(post_gallery_form);
}

async function post_gallery_form(e) {
    e.preventDefault();
    $("#gallery-form").unbind();
    let data = await $("#gallery-form").submit();
    console.log(data);
}