from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import model_to_dict

# Create your views here.
from django.db.models import Q
from django.shortcuts import render
from django.utils.datetime_safe import date
from django.views import generic, View
from ..models import Gallery, Images

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class GalleryListView(generic.ListView):
    model = Gallery

    template_name = 'photo_app/gallery_list.html'
    # context_object_name = 'gallery_list'

    def get(self, request):
        if request.user.is_staff:
            queryset = Gallery.objects.all()
        elif request.user.is_authenticated:
            queryset = Gallery.objects.filter(
                Q(Q(is_public=True, public_date__lte=date.today())) | Q(owner=request.user.id) |
                Q(photo_model__id=request.user.id) | Q(photographer=request.user))
        else:
            queryset = Gallery.objects.filter(is_public=True, public_date__lte=date.today())
        gallery_list = []
        for g in queryset:
            if g not in gallery_list:
                d = model_to_dict(g)
                if g.display_image is not None:
                    d['image'] = Images.objects.get(pk=g.display_image)
                gallery_list.append(d)
        return render(request, self.template_name, context={'gallery_list': gallery_list})
