from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.views.generic.edit import FormView
from django.urls import reverse_lazy

from ..forms import ProfileForm
from ..models import Gallery, Links, Release

import logging
logger = logging.getLogger(__name__)


class ProfileFormView(LoginRequiredMixin, FormView):
    form_class = ProfileForm
    image = None
    template_name = 'photo_app/profile.html'
    success_url = reverse_lazy('photo:profile')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['gallery_list'] = self.get_gallery_list()
        context['release_list'] = self.get_release_list()
        context['links'] = Links.objects.filter(user=self.request.user)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.request.user
        return kwargs

    def get_gallery_list(self):
        gallery_list = []
        gl = Gallery.objects.filter(Q(release__talent=self.request.user) | Q(owner=self.request.user) |
                                              Q(photographer=self.request.user)).order_by('shoot_date')
        for g in gl:
            if g not in gallery_list:
                gallery_list.append(g)
        return gallery_list

    def get_release_list(self):
        release_list = []
        rl = Release.objects.filter(Q(talent=self.request.user) | Q(photographer=self.request.user)).order_by('-shoot_date')
        for r in rl:
            if r not in release_list:
                release_list.append(r)
        return release_list

    def form_invalid(self, form):
        logging.warning(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        logging.warning(self.request.POST)
        logging.warning(form.cleaned_data)
        form.save()
        return super().form_valid(form)
