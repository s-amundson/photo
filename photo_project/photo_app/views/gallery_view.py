from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from ..models import Gallery
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class GalleryView(UserPassesTestMixin, ListView):
    gallery = None
    image_link = True
    model = Gallery
    template_name = 'photo_app/gallery.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['gallery'] = self.gallery
        context['image_link'] = self.image_link
        context['owner'] = self.gallery.owner == self.request.user
        context['models'] = self.get_models()
        return context

    def get_models(self):
        models = []
        for release in self.gallery.release.all():
            d = {}
            if release.use_full_name:
                d['name'] = release.talent_full_name
                d['links'] = release.talent.links_set.all()
            elif release.use_first_name:
                d['name'] = release.talent_first_name
            elif release.use_nickname:
                d['name'] = release.talent_nickname
            models.append(d)
        return models

    def get_queryset(self):
        queryset = self.gallery.images_set.filter(gallery=self.gallery).filter(privacy_level='public')
        logging.warning(queryset)
        return queryset.order_by('id')

    def test_func(self):
        self.gallery = get_object_or_404(Gallery, pk=self.kwargs.get('gallery_id'))
        if self.gallery.privacy_level == 'public':
            return True
        if self.request.user.is_authenticated:
            if self.gallery.privacy_level == 'authenticated':
                return True
            else:  # gallery is private
                if self.request.user == self.gallery.owner or self.request.user in self.gallery.photographer:
                    return True
        return False

class GalleryInsertView(GalleryView):
    image_link = False
    template_name = 'photo_app/gallery_insert.html'
