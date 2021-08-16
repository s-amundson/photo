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
    path('image', ImageView.as_view(), name='image'),
    path('image/<int:image_id>/', ImageView.as_view(), name='image'),
    path('image_get/<int:image_id>/', ImageGetView.as_view(), name='image_get'),
    path('image_upload/<int:gallery_id>/', ImageApiView.as_view(), name='image_upload'),
    path('links_form', LinksFormView.as_view(), name='links_form'),
    path('links_form/<int:link_id>/', LinksFormView.as_view(), name='links_form'),
    path('links_table/<int:user_id>/', LinksTableView.as_view(), name='links_table'),
    path('model_release/<int:release>/', ModelReleaseView.as_view(), name='model_release'),
    path('model_release', ModelReleaseView.as_view(), name='model_release'),
    path('privacy', PrivacyView.as_view(), name='privacy'),
    path('profile_info_api', PhotoModelApiView.as_view(), name='profile_info_api'),
    path('profile', ProfileView.as_view(), name='profile'),
    path('release_preview/<int:template>/', ReleaseTemplateView.as_view(), name='release_preview'),
    path('terms', TermsView.as_view(), name='terms'),
    path('thumb', ImageGetThumbView.as_view(), name='thumb'),
    path('thumb/<int:image_id>/', ImageGetThumbView.as_view(), name='thumb'),
]
