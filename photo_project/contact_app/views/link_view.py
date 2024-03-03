from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from ..models import Contact, Link
from ..forms import LinkForm

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class LinkView(UserPassesTestMixin, FormView):
    contact = None
    link = None
    form_class = LinkForm
    template_name = 'photo_app/form_as_p.html'
    success_url = reverse_lazy('contact:contact_list')

    def form_invalid(self, form):
        logging.warning(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        logging.info(form.cleaned_data)
        form.save()
        return super().form_valid(form)
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data()
    #     if self.contact is not None:
    #         context['links'] = self.contact.link_set.all()
    #     else:
    #         context['links'] = []
    #     return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.link is not None:
            kwargs['instance'] = self.link
        else:
            kwargs['initial']['person'] = self.contact
        logging.warning(kwargs)
        return kwargs

    def test_func(self):
        if self.request.user.is_authenticated:
            cid = self.kwargs.get('contact_id', None)
            lid = self.kwargs.get('link_id', None)
            self.contact = get_object_or_404(Contact, pk=cid)
            self.success_url = reverse_lazy('contact:contact', kwargs={'contact_id': cid})
            logging.warning(lid)
            if lid is not None:
                self.link = get_object_or_404(Link, pk=lid)
            return self.request.user.is_staff
        return False
