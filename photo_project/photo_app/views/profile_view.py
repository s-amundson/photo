from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.shortcuts import render
from django.views.generic.base import View
import logging

# from ..forms import PhotoModelForm
from ..models import Gallery
logger = logging.getLogger(__name__)


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        logging.debug(request.user)
        try:
            gallery_list = Gallery.objects.filter(Q(photo_model=request.user) | Q(owner=request.user))
        except Gallery.DoesNotExist:
            gallery_list = []
        # form = PhotoModelForm(initial=pm)
        return render(request, 'photo_app/profile.html', {'gallery_list': gallery_list})
