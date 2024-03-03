from django.contrib.auth.mixins import UserPassesTestMixin
# from django.forms import model_to_dict
# from django.db.models import Q
from django.views.generic import ListView
from ..forms import ContactSearchForm
from ..models import Contact

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class ContactListView(UserPassesTestMixin, ListView):
    model = Contact
    template_name = 'contact_app/contact_list.html'
    paginate_by = 100  # if pagination is desired
    form_class = ContactSearchForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.form_class(initial=self.request.GET)
        return context

    def get_queryset(self):
        form = self.form_class(self.request.GET)
        object_list = self.model.objects.all().order_by('first_name')
        if form.is_valid():
            if form.cleaned_data['last_name']:
                logging.debug(form.cleaned_data['last_name'])
                object_list = object_list.filter(last_name__icontains=form.cleaned_data['last_name'])
            if form.cleaned_data['first_name']:
                logging.debug(form.cleaned_data['first_name'])
                object_list = object_list.filter(first_name__icontains=form.cleaned_data['first_name'])
        return object_list

    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.is_staff
