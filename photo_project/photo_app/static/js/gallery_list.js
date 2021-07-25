"use strict";
var url_string = "gallery_form"
$(document).ready(function(){
    $("#div-add-gallery").hide();
    $("#btn-add-gallery").click(function(){
        load_gallery_form();
    });
});

