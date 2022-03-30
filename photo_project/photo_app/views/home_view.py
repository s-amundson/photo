from django.forms import model_to_dict
from django.db.models import Q
from django.utils.datetime_safe import date
from .gallery_list_view import GalleryListView
from ..models import Gallery, Images

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class HomeView(GalleryListView):

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['gallery_list'] = self.gallery_list
        context['home'] = True
        return context
