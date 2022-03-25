from django.contrib.auth.mixins import UserPassesTestMixin
from django.forms import model_to_dict
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import FormView
from django.http import JsonResponse

from ..models import Release
from ..forms import ReleasePhotographerForm, ReleaseModelForm, ReleaseSignedForm
from ..src.email import EmailMessage

# Get an instance of a logger
import logging
logger = logging.getLogger(__name__)


class ModelReleaseView(UserPassesTestMixin, FormView):
    form_class = ReleaseModelForm
    gallery = None
    template_name = 'photo_app/model_release.html'
    release = None
    success_url = reverse_lazy('photo:index')

    def form_invalid(self, form):
        logging.debug(self.form_class)
        logging.debug(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        logging.debug(form.cleaned_data)
        logging.debug(self.release)
        if self.release is None:
            mr = form.save()
            mr.state = 'pending'
            mr.photographer = self.request.user
            mr.save()
        elif self.release.state == 'pending' and self.release.photographer.id == self.request.user.id:
            mr = form.save()
            # EmailMessage().release_modified(self.release.talent, mr)

        elif self.release.state in ['pending', 'agreed'] and self.release.talent.id == self.request.user.id:
            mr = form.save()
            # if form.cleaned_data['agree']:
            if form.cleaned_data['talent_signature'] != form.empty_sig:
                logging.debug('signed')
                mr.state = 'agreed'
                mr.talent_first_name = self.request.user.first_name
                mr.talent_full_name = f'{self.request.user.first_name} {self.request.user.last_name}'
                mr.talent_nickname = self.request.user.nickname
                # mr.talent_signature = form.make_signature(
                #     f'{self.request.user.first_name}_{self.request.user.last_name}')
                mr.save()
            # EmailMessage().release_modified(self.release.photographer, mr)
        elif self.release.state == 'agreed':
            logging.debug(model_to_dict(self.release))
            if form.cleaned_data['photographer_signature'] != form.empty_sig:
                mr = form.save()
                mr.state = 'complete'
                mr.photographer_signature = form.make_signature(
                    f'{self.request.user.first_name}_{self.request.user.last_name}')
                mr.save()
        if form.cleaned_data.get('send_email', False):
            EmailMessage().release_notification(self.release.talent, mr)
            return render(self.request, 'photo_app/message.html', {'message': 'Release Saved'})
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.release is not None:
            kwargs['instance'] = self.release
        return kwargs

    def test_func(self):
        if self.request.user.is_authenticated:
            release = self.kwargs.get('release', None)
            if self.request.user.is_photographer and release is None:
                logging.debug('photographer')
                self.form_class = ReleasePhotographerForm
                return True
            else:
                self.release = get_object_or_404(Release, pk=release)
                logging.debug(self.release.state)
                logging.debug(model_to_dict(self.release))
                if self.request.user.id == self.release.photographer.id:
                    logging.debug('photographer')
                    if self.release.state == 'pending':
                        self.form_class = ReleasePhotographerForm
                    else:
                        self.form_class = ReleaseSignedForm
                    return True
                elif self.request.user.id == self.release.talent.id:
                    self.form_class = ReleaseModelForm
                    logging.debug('talent')
                    return True
                else:
                    return False
        else:
            return False


class ModelReleaseUpdateView(ModelReleaseView):
    def form_valid(self, form):
        logging.debug('update')
        if self.release is None:
            return self.form_invalid(form)
        mr = form.save()
        return JsonResponse({'status': 'success'})
