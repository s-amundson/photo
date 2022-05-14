from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from ..models import Contact
from ..forms import ContactForm

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class ContactView(UserPassesTestMixin, FormView):
    contact = None
    form_class = ContactForm
    template_name = 'contact_app/contact.html'
    success_url = reverse_lazy('contact:contact_list')

    def form_invalid(self, form):
        logging.warning(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        logging.info(form.cleaned_data)
        contact = form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        if self.contact is not None:
            context['comments'] = self.contact.comment_set.all()
            context['links'] = self.contact.link_set.all()
        else:
            context['comments'] = []
            context['links'] = []
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.contact is not None:
            kwargs['instance'] = self.contact
        return kwargs

    def test_func(self):
        if self.request.user.is_authenticated:
            cid = self.kwargs.get('contact_id', None)
            if cid is not None:
                self.contact = get_object_or_404(Contact, pk=cid)
            return self.request.user.is_staff
        return False
