import os
from PIL import Image

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseNotAllowed

# Create your views here.
from django.views import generic, View
from ..models import ReleaseTemplate
from ..forms import ReleaseTemplateForm, ReleaseTemplateChoiceForm
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class ReleaseTemplateFormView(LoginRequiredMixin, View):
    def get(self, request, release=None):
        if not request.user.is_photographer:
            return HttpResponseNotAllowed
        templates = ReleaseTemplateChoiceForm()
        form = ReleaseTemplateForm()

        return render(request, 'photo_app/release_template.html', {'form': form, 'templates': templates})

    def post(self, request, release=None):
        logging.debug('here')
        if not request.user.is_photographer:
            return HttpResponseNotAllowed
        if release is not None:
            instance = get_object_or_404(ReleaseTemplate, pk=release)
        else:
            instance = None
        logging.debug(instance)
        form = ReleaseTemplateForm(request.POST, request.FILES, instance=instance)
        if form.is_valid():
            logging.debug(form.cleaned_data)
            form.save()

        else:
            logging.debug(form.errors)
        templates = ReleaseTemplateChoiceForm()
        return render(request, 'photo_app/release_template.html', {'form': form, 'templates': templates})


class ReleaseTemplateView(LoginRequiredMixin, View):
    def get(self, request, release=None):
        if not request.user.is_photographer:
            return HttpResponseNotAllowed

        logging.debug('here')
        template_file = get_object_or_404(ReleaseTemplate, pk=release)
