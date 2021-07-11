import os
from PIL import Image

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseNotAllowed, HttpResponse, HttpResponseRedirect

# Create your views here.
from django.template.loader import get_template
from django.views import generic, View
from ..models import Release
from ..forms import ReleasePhotographerForm, ReleaseModelForm, ReleaseSignedForm
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class ModelReleaseView(LoginRequiredMixin, View):
    def get(self, request, release=None):
        logging.debug(release)
        request.session['model_release'] = release
        if request.user.is_photographer and release == 0:
            form = ReleasePhotographerForm()
        else:
            r = get_object_or_404(Release, pk=release)
            logging.debug(r)
            if request.user.id == r.photographer.id:
                if r.state == 'pending':
                    form = ReleasePhotographerForm(instance=r)
                else:
                    form = ReleaseSignedForm(instance=r)

            elif request.user.id == r.photo_model.id:
                form = ReleaseModelForm(instance=r)

        return render(request, 'photo_app/model_release.html', {'use_form': form})

    def post(self, request, release=0):
        logging.debug(release)
        logging.debug(request.POST)
        request.session['model_release'] = release
        if release == 0:

            form = ReleasePhotographerForm(request.POST)
        else:
            instance = get_object_or_404(Release, pk=release)
            if request.user.id == instance.photographer.id:
                logging.debug('ReleasePhotographerForm')
                form = ReleasePhotographerForm(request.POST, instance=instance)
            elif request.user.id == instance.photo_model.id:
                logging.debug('ReleaseModelForm')
                form = ReleaseModelForm(request.POST, instance=instance)
            else:
                return HttpResponseNotAllowed

        if form.is_valid():
            logging.debug(form.cleaned_data)
            if release == 0:
                mr = form.save()
                mr.state = 'pending'
                mr.photographer = request.user
                mr.save()
                logging.debug(mr)

            elif instance.state == 'pending' and instance.photographer.id == request.user.id:
                r = form.save()
                logging.debug(r)
            elif instance.state in ['pending', 'agreed'] and instance.photo_model.id == request.user.id:
                mr = form.save()
                if form.cleaned_data['agree']:
                    mr.state = 'agreed'
                    mr.model_first_name = request.user.first_name
                    mr.model_full_name = f'{request.user.first_name} {request.user.last_name}'
                    mr.model_nickname = request.user.nickname
                    mr.save()
            elif form.state == 'agreed':
                instance.file = form.file
                instance.save()
            if form.cleaned_data.get('send_email', False):
                return render(request, 'photo_app/message.html', {'message': 'Release Saved'})
            return render(request, 'photo_app/model_release.html', {'use_form': form})

        else:
            logging.debug(form.errors)
        return render(request, 'photo_app/model_release.html', {'form': form, 'title': 'Model Release'})


