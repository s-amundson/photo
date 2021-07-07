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
from PIL import Image

from ..forms import GalleryForm
from ..models import Gallery
from ..serializers import ImageSerializer

logger = logging.getLogger(__name__)


class ImageApiView(LoginRequiredMixin, APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, gallery_id):
        logging.debug(request.data)

        serializer = ImageSerializer(data=request.data)
        if serializer.is_valid():
            # logging.debug(serializer.validated_data)
            # img = serializer.validated_data.get('image')
            # img = Image.open(serializer.validated_data.get('image'))
            # w, h = img.size
            # logging.debug(f'width= {w}, height= {h}')
            # exif = img.getexif()
            # logging.debug(exif)

            # image_form = serializer.save(height=h, width=w, thumb_width=100, orientation=exif[274])
            image_form = serializer.save()

            return Response(serializer.data)

        else:
            logging.debug(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
