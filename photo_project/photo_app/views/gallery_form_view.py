from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic.edit import FormView
from django.core.exceptions import PermissionDenied
from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.urls import reverse
from django.views.generic.base import View

from django.http import JsonResponse
import logging
from django.http import HttpResponse, HttpResponseBadRequest

from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

from ..forms import GalleryForm
from ..models import Gallery
from ..serializers import GallerySerializer

logger = logging.getLogger(__name__)


# class GalleryFormApiView(LoginRequiredMixin, APIView):
#     permission_classes = [permissions.IsAuthenticated]
#
#     def post(self, request, gallery_id=None):
#
#         if gallery_id is not None:
#             g = get_object_or_404(Gallery, pk=gallery_id)
#             logging.debug(g.owner)
#             if not request.user == g.owner or request.user.is_superuser:
#                 return HttpResponseBadRequest()
#             # serializer = GallerySerializer()
#         else:
#             g = None
#         logging.debug('here')
#         serializer = GallerySerializer(data=request.data)
#         if serializer.is_valid():
#             logging.debug('valid')
#             if gallery_id is None:
#                 gallery = serializer.save()
#                 gallery.owner = request.user
#                 gallery.save()
#                 logging.debug(gallery)
#             return Response(serializer.data)
#
#         else:
#             logging.debug(serializer.errors)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GalleryFormView(UserPassesTestMixin, FormView):
    form_class = GalleryForm
    gallery = None
    template_name = 'photo_app/forms/gallery_form.html'

    def form_invalid(self, form):
        logging.debug(form.errors)
        return JsonResponse({'status': 'ERROR', 'errors': form.errors})

    def form_valid(self, form):
        logging.debug(form.cleaned_data)
        gallery = form.save(commit=False)
        if self.gallery is None:
            gallery.owner = self.request.user
        gallery.save()
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
