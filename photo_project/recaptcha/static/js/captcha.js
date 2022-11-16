"use strict";
$(document).ready(function(){
    $(".captcha-link").click(async function(e) {
        e.preventDefault();
        await post_recapcha_href($(this).attr('href'), false);
    });
});

async function post_recapcha_href(href, as_json) {
    let action = 'galleries';
    console.log(href)
    if (href != "/") {

        while (href.slice(-1) == "/") {
            href = href.substring(0, href.length - 1)
            console.log(href)
        }
        let arr = href.split("/")
        action = arr[arr.length - 1]

    }

    grecaptcha.ready(function() {
        grecaptcha.execute(recaptcha_site_v3, {action: action}).then(async function(token) {
            if (as_json) {
                let data = await $.post(url_recaptcha, {
                    csrfmiddlewaretoken: $("#recaptcha-form_v3").find('[name="csrfmiddlewaretoken"]').val(),
                    captcha: token,
                    url: href,
                }, function(data, status) {
                return data;
                }, "json");
            } else {
                $("#recaptcha-form_v3").find("#id_captcha").val(token)
                $("#recaptcha-form_v3").find("#id_url").val(href)
                $("#recaptcha-form_v3").submit()
            }
        });
    });
}

async function recaptchaCallback() {
    if ($.inArray(window.location.pathname, recaptcha_url_list) >=0) {
        console.log(window.location.pathname);
        post_recapcha_href(window.location.pathname, true)
    }
}