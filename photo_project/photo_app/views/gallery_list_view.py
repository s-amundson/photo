from django.forms import model_to_dict
from django.db.models import Q
from django.utils import timezone
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
        context['carousel_images'] = Images.objects.filter(carousel=True, privacy_level="public", )
        if self.request.user.is_authenticated:
            context['carousel_images'] = context['carousel_images'].filter(
                gallery__privacy_level__in=["public", 'authenticated'])
        else:
            context['carousel_images'] = context['carousel_images'].filter(gallery__privacy_level="public")
        logger.warning(context['carousel_images'])
        return context

    def get_queryset(self):
        if self.request.user.is_staff:
            logger.warning('staff')
            queryset = Gallery.objects.all()
        elif self.request.user.is_authenticated:
            logger.warning('authenticated')
            queryset = Gallery.objects.filter(
                Q(Q(privacy_level__in=['public', 'authenticated'], public_date__lte=timezone.datetime.today())) |
                Q(owner=self.request.user.id) |
                Q(release__talent__id=self.request.user.id) |
                Q(photographer=self.request.user))
        else:
            logger.warning('not auth')
            queryset = Gallery.objects.filter(privacy_level='public', public_date__lte=timezone.datetime.today())
        self.gallery_list = []

        queryset = queryset.order_by("-id")
        logging.warning(queryset)
        for g in queryset:
            if g not in self.gallery_list:
                d = model_to_dict(g)
                if g.display_image is not None:
                    d['image'] = g.display_image
                self.gallery_list.append(d)
        logging.warning(len(self.gallery_list))
