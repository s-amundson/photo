from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.http import HttpResponseRedirect
from django.urls import reverse
import logging

from ..models import PhotoModel
from ..forms import PhotoModelForm
logger = logging.getLogger(__name__)


class ModelInfoView(LoginRequiredMixin, View):

    def get(self, request):
        try:
            pm = PhotoModel.objects.get(user=request.user)
            form = PhotoModelForm(initial=pm)
        except PhotoModel.DoesNotExist:
            form = PhotoModelForm()

        return render(request, 'photo_app/forms/model_form.html', {'form': form})
