from django.urls import path
from .views import *
app_name = 'recaptcha'
urlpatterns = [
    path('v3/', RecaptchaThreeView.as_view(), name='v3'),
]
