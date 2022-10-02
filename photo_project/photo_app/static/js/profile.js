"use strict";
$(document).ready(function() {
    $("#profile-form-div").hide();
    $("#btn-address-edit").click(function () {
        $("#profile-address").hide();
        $("#profile-form-div").show();
    });
    $("#btn-add-link").click(function () {
        console.log('load_link_form')
        load_link_form('');
    });
});
