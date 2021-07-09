import os
from PIL import Image

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseNotAllowed, HttpResponse

# Create your views here.
from django.template.loader import get_template
from django.views import generic, View
from ..models import Release
from ..forms import ReleaseTemplateForm, ReleaseTemplateChoiceForm, ReleasePhotographerForm
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class ModelReleaseView(LoginRequiredMixin, View):
    def get(self, request, release):
        if release == 0:
            form = ReleasePhotographerForm()
        else:
            form = ReleasePhotographerForm(instance=get_object_or_404(Release, pk=release))

        return render(request, 'photo_app/release_template.html', {'form': form})

    def post(self, request, release):
        logging.debug('here')
        if release == 0:
            form = ReleasePhotographerForm(request.POST)
        else:
            instance = get_object_or_404(Release, pk=release)
            form = ReleasePhotographerForm(request.POST, instance=instance)

        if form.is_valid():
            logging.debug(form.cleaned_data)
            if release == 0:
                form.save(commit=False)
                form.photographer = request.user
            form.save()

        else:
            logging.debug(form.errors)
        # TODO change this to acutal template
        return render(request, 'photo_app/release_template.html', {'form': form})


