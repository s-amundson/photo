from django.contrib.auth.mixins import UserPassesTestMixin
# from django.forms import model_to_dict
# from django.db.models import Q
# from django.utils.datetime_safe import date
from django.views.generic import ListView
from ..models import Contact

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class ContactListView(UserPassesTestMixin, ListView):
    model = Contact

    template_name = 'contact_app/contact_list.html'

    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.is_staff
