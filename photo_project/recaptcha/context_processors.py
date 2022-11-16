from django.conf import settings
from .forms import RecaptchaFormV3


def recaptcha(request):
    return {
        'RECAPTCHA_SITE_KEY_V2': settings.RECAPTCHA_PUBLIC_KEY,
        "RECAPTCHA_SITE_KEY_V3": settings.RECAPTCHA_SITE_KEY_V3,
        "recaptcha3_form": RecaptchaFormV3(),
    }
