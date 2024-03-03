"use strict";
$(document).ready(function() {
    $(".gallery").click(function () {
        $.get($(this).attr("url"), function(data, status){
            $("#gallery-images").html(data);
            image_event();
        });
    });
    $(".reference-image").click(function () {
        $("#id_reference_image").val($(this).attr("img_id"));
        hide_select_images(true);
        $("#selected-image").html($(this).clone().width("500"));
        $("#image-input-div").hide();
    });
    $("#id_reference_image").change(function (){
        console.log('change');
        if ($(this).val() == '') {
            hide_select_images(false);
            $("#selected-image").html("");
            $("#image-input-div").show();
        }
    });

    image_event();
    $("#id_image").change(function (){
        console.log('change');
        if ($(this).val() == '') {
            hide_select_images(false);
            $("#selected-image").html("");
            $("#reference-image-input-div").show();
        }
    });
    $(".mood-image").click(function () {
        let selected_array = $("#id_mood_image").val();
        if ($.inArray("" + $(this).attr("img_id"), selected_array) >= 0) {
            selected_array.pop($(this).attr("img_id"));
            $(this).css("background-color", "#212529");
        } else {
            selected_array.push("" + $(this).attr("img_id"))
            $(this).css("background-color", "#343a40");
        }
        $("#id_mood_image").val(selected_array);
    });
    $("#id_mood_image").change(function(){
        let selected_array = $("#id_mood_image").val();
        $(".mood-image").each(function(i, el ) {
            if ($.inArray("" + $(el).attr("img_id"), selected_array) >= 0) {
                $(this).css("background-color", "#343a40");
            } else {
                $(this).css("background-color", "#212529");
            }
        });
    });
});

function hide_select_images(hide) {
    if (hide) {
        $("#reference-images-div").hide();
        $("#gallery-list").hide();
        $("#gallery-images").hide();
    } else {
        $("#reference-images-div").show();
        $("#gallery-list").show();
        $("#gallery-images").show();
    }
}

function image_event() {
    $(".gallery-image").click(function () {
        $("#id_image").val($(this).attr("img_id"));
        hide_select_images(true);
        $("#selected-image").html($(this).clone().width("500"));
        $("#reference-image-input-div").hide();
    });
}