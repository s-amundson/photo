from django.urls import path
from .views import *
app_name = 'photo'
urlpatterns = [
    path('', GalleryListView.as_view(), name='index'),
    path('gallery_form', GalleryFormView.as_view(), name='gallery_form'),
    path('gallery_form/<int:gallery_id>/', GalleryFormView.as_view(), name='gallery_form'),
    path('gallery_form_api/<int:gallery_id>/', GalleryFormApiView.as_view(), name='gallery_form_api'),
    path('gallery_form_api', GalleryFormApiView.as_view(), name='gallery_form_api'),
    path('gallery_view/<int:gallery_id>/', GalleryView.as_view(), name='gallery_view'),
    path('image_upload/<int:gallery_id>/', ImageApiView.as_view(), name='image_upload'),
    path('model_release/<int:release>/', ModelReleaseView.as_view(), name='model_release'),
    path('model_release', ModelReleaseView.as_view(), name='model_release'),
    path('profile_info_api', PhotoModelApiView.as_view(), name='profile_info_api'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('release_preview/<int:template>/', ReleaseTemplateView.as_view(), name='release_preview'),
    path('release_template/<int:template>/', ReleaseTemplateFormView.as_view(), name='release_template'),
    path('release_template', ReleaseTemplateFormView.as_view(), name='release_template'),
]
