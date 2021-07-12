
from django.contrib.auth.mixins import LoginRequiredMixin
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseBadRequest

# Create your views here.

from django.views import View
from ..models import Release
from ..forms import ReleasePhotographerForm, ReleaseModelForm, ReleaseSignedForm
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class ModelReleaseView(LoginRequiredMixin, View):
    def get(self, request, release=None):
        logging.debug(release)
        request.session['model_release'] = release
        if request.user.is_photographer and release is None:
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
            else:
                return HttpResponseBadRequest()
        return render(request, 'photo_app/model_release.html', {'use_form': form})

    def post(self, request, release=0):
        logging.debug(release)
        logging.debug(request.POST)
        request.session['model_release'] = release
        if release == 0:

            form = ReleasePhotographerForm(request.POST)
        else:
            instance = get_object_or_404(Release, pk=release)
            logging.debug(instance.photo_model.id)
            if request.user.id == instance.photographer.id:
                if instance.state == 'pending':
                    logging.debug('ReleasePhotographerForm')
                    form = ReleasePhotographerForm(request.POST, instance=instance)
                else:
                    form = ReleaseSignedForm(request.POST, request.FILES, instance=instance)
            elif request.user.id == instance.photo_model.id:
                logging.debug('ReleaseModelForm')
                form = ReleaseModelForm(request.POST, instance=instance)
            else:
                return HttpResponseBadRequest()
        # logging.debug(model_to_dict(instance))
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
            elif instance.state == 'agreed':
                logging.debug(model_to_dict(instance))
                mr = form.save()
                mr.state = 'complete'
                mr.save()
            if form.cleaned_data.get('send_email', False):
                return render(request, 'photo_app/message.html', {'message': 'Release Saved'})
            return render(request, 'photo_app/model_release.html', {'use_form': form})

        else:
            logging.debug(form.errors)
        return render(request, 'photo_app/model_release.html', {'form': form, 'title': 'Model Release'})
