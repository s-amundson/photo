from django.urls import path
from .views import *
app_name = 'contact_app'
urlpatterns = [
    path('comment/<int:contact_id>/', CommentView.as_view(), name='comment'),
    path('comment/<int:contact_id>/<int:comment_id>/', CommentView.as_view(), name='comment'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('contact/<int:contact_id>/', ContactView.as_view(), name='contact'),
    path('contact_list/', ContactListView.as_view(), name='contact_list'),
    path('link/<int:contact_id>/', LinkView.as_view(), name='link'),
    path('link/<int:contact_id>/<int:link_id>/', LinkView.as_view(), name='link'),
]
