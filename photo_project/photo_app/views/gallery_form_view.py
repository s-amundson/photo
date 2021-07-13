from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse
from django.views.generic.base import View
from django.http import JsonResponse
import logging
from django.http import HttpResponseBadRequest

from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

from ..forms import GalleryForm
from ..models import Gallery
from ..serializers import GallerySerializer

logger = logging.getLogger(__name__)


class GalleryFormApiView(LoginRequiredMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, gallery_id=None):
        logging.debug('here')
        if gallery_id is not None:
            g = get_object_or_404(Gallery, pk=gallery_id)
            if request.user == g.owner or request.user.is_superuser:
                pass
            else:
                return HttpResponseBadRequest()
            # serializer = GallerySerializer()
        else:
            g = None

        serializer = GallerySerializer(data=request.data)
        if serializer.is_valid():
            if gallery_id is None:
                gallery = serializer.save()
                gallery.owner = request.user
                gallery.save()
            return Response(serializer.data)

        else:
            logging.debug(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GalleryFormView(LoginRequiredMixin, View):
    def get_instance(self, request, gallery_id):
        if gallery_id is not None:
            g = get_object_or_404(Gallery, pk=gallery_id)
            if request.user == g.owner or request.user.is_superuser:
                pass
            else:
                raise PermissionDenied
        else:
            g = None
        return g

    def get(self, request, gallery_id=None):
        logging.debug('here')
        try:
            g = self.get_instance(request, gallery_id)
        except PermissionDenied:
            return HttpResponseBadRequest()
        form = GalleryForm(instance=g)

        return render(request, 'photo_app/forms/gallery_form.html', {'form': form})

    def post(self, request, gallery_id=None):
        logging.debug(request.POST)
        logging.debug(gallery_id)
        try:
            g = self.get_instance(request, gallery_id)
        except PermissionDenied:
            return HttpResponseBadRequest()
        form = GalleryForm(request.POST, instance=g)
        # form.clean()
        # logging.debug(form.cleaned_data)

        if form.is_valid():
            logging.debug(form.cleaned_data)
            gallery = form.save(commit=False)
            if gallery_id is None:
                gallery.owner = request.user
            gallery.save()
            url = reverse('photo_app:gallery_view', kwargs={'gallery_id': gallery.id})
            return JsonResponse({'status': "SUCCESS", 'url': url})
        else:
            logging.debug(form.errors)
            return JsonResponse({'status': 'ERROR', 'errors': form.errors})
