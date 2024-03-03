from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy

from ..models import Comment, Contact, Link
from ..forms import CommentForm

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class CommentView(UserPassesTestMixin, FormView):
    comment = None
    contact = None
    form_class = CommentForm
    template_name = 'photo_app/form_as_p.html'
    success_url = reverse_lazy('contact:contact_list')

    def form_invalid(self, form):
        logging.warning(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        logging.info(form.cleaned_data)
        form.save()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.comment is not None:
            kwargs['instance'] = self.comment
        else:
            kwargs['initial']['person'] = self.contact
        logging.warning(kwargs)
        return kwargs

    def test_func(self):
        if self.request.user.is_authenticated:
            cid = self.kwargs.get('contact_id', None)
            com_id = self.kwargs.get('comment_id', None)
            self.contact = get_object_or_404(Contact, pk=cid)
            self.success_url = reverse_lazy('contact:contact', kwargs={'contact_id': cid})
            logging.warning(com_id)
            if com_id is not None:
                self.comment = get_object_or_404(Comment, pk=com_id)
            return self.request.user.is_staff
        return False
