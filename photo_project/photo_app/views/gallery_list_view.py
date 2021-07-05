from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
from django.shortcuts import render
from django.views import generic, View
from ..models import Gallery

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class GalleryListView(LoginRequiredMixin, generic.ListView):
    model = Gallery

    template_name = 'photo_app/gallery_list.html'
    # context_object_name = 'gallery_list'

    def get(self, request):
        queryset = Gallery.objects.filter(owner=request.user.id)
        return render(request, self.template_name, context={'gallery_list': queryset})
