from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404
from django.template.loader import get_template
from django.views.generic.base import View
from django.http import JsonResponse
import logging
from django.http import HttpResponseBadRequest

from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response

from ..forms import LinkForm
from ..models import Links, User
from ..serializers import LinkSerializer

logger = logging.getLogger(__name__)


# class LinksApiView(LoginRequiredMixin, APIView):
#     permission_classes = [permissions.IsAuthenticated]
#
#     def post(self, request, link_id):
#         logging.debug(request.data)
#
#         serializer = LinkSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#
#             return Response(serializer.data)
#
#         else:
#             logging.debug(serializer.errors)
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LinksFormView(LoginRequiredMixin, View):
    def get(self, request, link_id=None):
        if link_id:
            link = get_object_or_404(Links, pk=link_id, user=request.user)
            link_form = LinkForm(instance=link)
        else:
            link_form = LinkForm()
        return render(request, 'photo_app/forms/link_form.html', {'link_form': link_form})

    def post(self, request, link_id=None):
        if link_id:
            link = get_object_or_404(Links, pk=link_id, user=request.user)
            link_form = LinkForm(request.POST, instance=link)
        else:
            link_form = LinkForm(request.POST)
        if link_form.is_valid():
            l = link_form.save(commit=False)
            l.user = request.user
            l.save()
            return JsonResponse(model_to_dict(l))
        else:
            logging.debug(link_form.errors)
            return JsonResponse(link_form.errors)


class LinksTableView(View):
    def get(self, request, user_id):
        logging.debug(user_id)
        u = get_object_or_404(User, pk=user_id)
        links = Links.objects.filter(user=u)
        return render(request, 'photo_app/tables/links_table.html',
                      {'links': links, 'owner': True if u == request.user else False})
