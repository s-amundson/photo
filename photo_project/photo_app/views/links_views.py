from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import FormView
from django.views.generic.base import View
from django.http import JsonResponse
from django.urls import reverse_lazy

from ..forms import LinkForm
from ..models import Links, User

import logging
logger = logging.getLogger(__name__)


class LinkCategoryCreateView(UserPassesTestMixin, CreateView):
    model = Links
    fields = ['category']
    template_name = 'photo_app/form_as_p.html'

    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.is_staff


class LinkCategoryUpdateView(UserPassesTestMixin, UpdateView):
    model = Links
    fields = ['category']
    template_name = 'photo_app/form_as_p.html'

    def test_func(self):
        if self.request.user.is_authenticated:
            return self.request.user.is_staff


class LinksFormView(LoginRequiredMixin, FormView):
    form_class = LinkForm
    template_name = 'photo_app/forms/link_form.html'
    success_url = reverse_lazy('photo:index')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        link_id = self.kwargs.get('link_id', None)
        if link_id is not None:
            kwargs['instance'] = get_object_or_404(Links, pk=link_id, user=self.request.user)
        return kwargs

    def form_invalid(self, form):
        logging.debug(form.errors)
        return JsonResponse(form.errors)

    def form_valid(self, form):
        l = form.save(commit=False)
        l.user = self.request.user
        l.save()
        return JsonResponse(model_to_dict(l))


class LinksTableView(View):
    def get(self, request, user_id):
        logging.debug(user_id)
        u = get_object_or_404(User, pk=user_id)
        links = Links.objects.filter(user=u)
        return render(request, 'photo_app/tables/links_table.html',
                      {'links': links, 'owner': True if u == request.user else False})
