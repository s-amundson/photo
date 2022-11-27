from django.urls import path
from .views import *
app_name = 'reference'
urlpatterns = [
    path('category/', CategoryView.as_view(), name='category'),
    path('image_get/', ReferenceImageGetView.as_view(), name='image_get'),
    path('image_get/<int:ref_id>/', ReferenceImageGetView.as_view(), name='image_get'),
    path('mood_form/', MoodFormView.as_view(), name='mood_form'),
    path('mood_form/<int:ref_id>/', MoodFormView.as_view(), name='mood_form'),
    path('mood_image/', MoodImageView.as_view(), name='mood_image'),
    path('mood_image/<int:ref_id>/', MoodImageView.as_view(), name='mood_image'),
    path('mood_list/', MoodListView.as_view(), name='mood_list'),
    path('mood_page/<str:ref>', MoodPageView.as_view(), name='mood_page'),
    path('reference_form/', ReferenceFormView.as_view(), name='reference_form'),
    path('reference_form/<int:ref_id>/', ReferenceFormView.as_view(), name='reference_form'),
    path('reference_list/', ReferenceListView.as_view(), name='reference_list'),
]
