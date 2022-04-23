"use strict";
$(document).ready(function() {
    get_comments(url_image_comment);
});

function get_comments(url) {
    $.get(url, function(data, status){
        $("#div-image-comment").html(data);
    });
}
