from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, FormView

from src.mixins import StaffMixin
from ..forms import MoodForm, MoodImageForm
from ..models import Mood, MoodImage, Reference
from photo_app.models import Gallery

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class MoodFormView(StaffMixin, FormView):
    form_class = MoodForm
    success_url = reverse_lazy('reference:mood_list')

    template_name = 'reference_images/mood_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_list'] = MoodImage.objects.all()
        logging.warning(context)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if 'ref_id' in self.kwargs:
            kwargs['instance'] = get_object_or_404(Mood, pk=self.kwargs['ref_id'])
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class MoodImageView(StaffMixin, FormView):
    form_class = MoodImageForm
    success_url = reverse_lazy('reference:mood_list')
    template_name = 'reference_images/mood_image.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reference_images'] = Reference.objects.filter(active=True).order_by('id')
        context['galleries'] = Gallery.objects.all()
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if 'ref_id' in self.kwargs:
            kwargs['instance'] = get_object_or_404(MoodImage, pk=self.kwargs['ref_id'])
        return kwargs

    def form_valid(self, form):
        form.save()
        self.success_url = self.request.GET.get('next', self.success_url)
        return super().form_valid(form)


class MoodListView(StaffMixin, ListView):
    model = Mood
    template_name = 'reference_images/mood_list.html'

    def get_context_data(self):
        context = super().get_context_data()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        logging.warning(queryset)
        return queryset.order_by('id')


class MoodPageView(ListView):
    model = Mood
    template_name = 'reference_images/mood_page.html'

    def get_queryset(self):
        mood = get_object_or_404(Mood, random_url=self.kwargs.get('ref'), is_public=True)
        queryset = mood.mood_image.all()
        return queryset
