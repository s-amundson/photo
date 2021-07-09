import os
from PIL import Image

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseNotAllowed, HttpResponse

# Create your views here.
from django.template.loader import get_template
from django.views import generic, View
from ..models import ReleaseTemplate
from ..forms import ReleaseTemplateForm, ReleaseTemplateChoiceForm, ReleasePhotographerForm
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class ReleaseTemplateFormView(LoginRequiredMixin, View):
    def get(self, request, release=None):
        if not request.user.is_photographer:
            return HttpResponseNotAllowed
        templates = ReleaseTemplateChoiceForm()
        form = ReleaseTemplateForm()
        use_form = ReleasePhotographerForm()

        return render(request, 'photo_app/release_template.html',
                      {'form': form, 'templates': templates, 'use_form': use_form})

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
    def get(self, request, release):
        if not request.user.is_photographer:
            return HttpResponseNotAllowed

        logging.debug('here')
        rt = get_object_or_404(ReleaseTemplate, pk=release)
        release_txt = os.path.join(settings.BASE_DIR, 'photo_app', 'templates', 'release.txt')
        lines = []
        for line in rt.file.readlines():
            lines.append(f"<p>{line.decode('UTF-8')}</p>")
        with open(release_txt, 'w') as t:
            t.writelines(lines)
        template = get_template('release.txt').render(
            {'photographer': f'{request.user.first_name} {request.user.last_name}'})
        os.remove(release_txt)

        return HttpResponse(template, content_type="text/plain")
