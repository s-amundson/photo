"""photo_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from photo_app.views import SignupView

urlpatterns = [
    path('accounts/signup/', SignupView.as_view(), name="account_signup"),
    path('accounts/', include('allauth.urls')),
    path('admin/', admin.site.urls),
    path('', include('photo_app.urls', namespace='photo_app')),
    path('contact/', include('contact_app.urls', namespace='contact')),
    path('recaptcha/', include('recaptcha.urls', namespace='recaptcha')),
    path('reference/', include('reference_images.urls', namespace='reference')),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG :
#     urlpatterns += patterns('',
#         (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
#     )
