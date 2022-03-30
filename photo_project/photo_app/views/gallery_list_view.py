from django.forms import model_to_dict
from django.db.models import Q
from django.utils.datetime_safe import date
from django.views.generic import ListView
from ..models import Gallery, Images

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class GalleryListView(ListView):
    model = Gallery

    template_name = 'photo_app/gallery_list.html'
    gallery_list = []

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['gallery_list'] = self.gallery_list
        return context

    def get_queryset(self):
        if self.request.user.is_staff:
            queryset = Gallery.objects.all()
        elif self.request.user.is_authenticated:
            queryset = Gallery.objects.filter(
                Q(Q(is_public=True, public_date__lte=date.today())) | Q(owner=self.request.user.id) |
                Q(release__talent__id=self.request.user.id) | Q(photographer=self.request.user))
        else:
            queryset = Gallery.objects.filter(is_public=True, public_date__lte=date.today())
        self.gallery_list = []
        for g in queryset:
            if g not in self.gallery_list:
                d = model_to_dict(g)
                if g.display_image is not None:
                    d['image'] = g.display_image
                self.gallery_list.append(d)
        logging.debug(len(self.gallery_list))
