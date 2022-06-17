from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404
from django.urls import reverse

from django.http import JsonResponse
import logging

from ..forms import GalleryForm
from ..models import Gallery

logger = logging.getLogger(__name__)


class GalleryFormView(UserPassesTestMixin, FormView):
    form_class = GalleryForm
    gallery = None
    template_name = 'photo_app/forms/gallery_form.html'

    def form_invalid(self, form):
        logging.warning(form.errors)
        return JsonResponse({'status': 'ERROR', 'errors': form.errors})

    def form_valid(self, form):
        logging.warning(self.request.POST)
        logging.info(form.cleaned_data)
        gallery = form.save(commit=False)
        if self.gallery is None:
            gallery.owner = self.request.user
        logging.debug(gallery.is_mature)
        if gallery.is_mature and gallery.privacy_level == 'public':
            gallery.privacy_level = 'authenticated'
        gallery.save()
        form.save_m2m()
        url = reverse('photo_app:gallery_view', kwargs={'gallery_id': gallery.id})
        return JsonResponse({'status': "SUCCESS", 'url': url})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        logging.debug(self.kwargs.get('gallery_id', None))
        context['update'] = self.kwargs.get('gallery_id', None) is not None
        logging.debug(context)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.gallery is not None:
            kwargs['instance'] = self.gallery
        return kwargs

    def test_func(self):
        if self.request.user.is_authenticated:
            gid = self.kwargs.get('gallery_id', None)
            logging.debug(gid)
            if gid is not None:
                self.gallery = get_object_or_404(Gallery, pk=gid)
                # if not (self.request.user == gid.owner or self.request.user.is_superuser):
                #     return False
            return self.request.user.is_staff
        else:
            return False
