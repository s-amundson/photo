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
    path('image_upload', ImageApiView.as_view(), name='image_upload'),
    path('model_info', ModelInfoView.as_view(), name='model_info'),
    path('model_info_api', PhotoModelApiView.as_view(), name='model_info'),
    path('profile', ProfileView.as_view(), name='profile'),
]
