from django.contrib.sites.models import Site
from django.shortcuts import render
from django.views.generic.base import View


class AboutView(View):
    def get(self, request):
        return render(request, 'photo_app/about_me.html')
