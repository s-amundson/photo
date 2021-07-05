from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
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
    def get(self, request, gallery_id=None):
        logging.debug('here')
        if gallery_id is not None:
            g = get_object_or_404(Gallery, pk=gallery_id)
        else:
            g = None
        form = GalleryForm(initial=g)

        return render(request, 'photo_app/forms/gallery_form.html', {'form': form})

    def post(self, request, gallery_id=None):
        logging.debug(request.POST)
        form = GalleryForm(request.POST)
        # form.clean()
        # logging.debug(form.cleaned_data)

        if form.is_valid():
            gallery = form.save(commit=False)
            gallery.owner = request.user
            gallery.save()
            return JsonResponse({'status': "SUCCESS"})
        else:
            return JsonResponse({'status': 'ERROR', 'errors': form.errors})
