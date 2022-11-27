from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, FormView
from django_sendfile import sendfile

from src.mixins import StaffMixin
from ..forms import ReferenceForm
from ..models import Reference

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class ReferenceFormView(StaffMixin, FormView):
    form_class = ReferenceForm
    success_url = reverse_lazy('reference:reference_list')
    template_name = 'reference_images/reference.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if 'ref_id' in self.kwargs:
            kwargs['instance'] = get_object_or_404(Reference, pk=self.kwargs['ref_id'])
        return kwargs

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ReferenceImageGetView(View):
    def get(self, request, ref_id, thumb=False):
        image = get_object_or_404(Reference, pk=ref_id)
        return sendfile(request, image.image.path)


class ReferenceListView(StaffMixin, ListView):
    model = Reference
    template_name = 'reference_images/reference_list.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['form'] = ReferenceForm()
        return context

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset.filter(active=True).order_by('id')
        return queryset
