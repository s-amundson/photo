from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic.base import View
import logging

# from ..forms import PhotoModelForm
from ..models import Gallery, PhotoModel
logger = logging.getLogger(__name__)


class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        try:
            pm = PhotoModel.objects.get(user=request.user)
            gallery_list = Gallery.objects.filter(photo_model=request.user.id)
        except PhotoModel.DoesNotExist:
            pm = None
            gallery_list = None
        # form = PhotoModelForm(initial=pm)
        return render(request, 'photo_app/profile.html', {'photo_model': pm, 'gallery_list': gallery_list})
