# import os
# from PIL import Image
# from allauth.account.models import EmailAddress
#
# from django.conf import settings
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.shortcuts import get_object_or_404, render, redirect
# from django.http import HttpResponseNotAllowed, HttpResponse
#
# # Create your views here.
# from django.template.loader import get_template
# from django.views import generic, View
# from ..models import ReleaseTemplate, User, Release
# from ..forms import ReleaseTemplateForm, ReleaseTemplateChoiceForm, ReleasePhotographerForm
# import logging
#
# # Get an instance of a logger
# logger = logging.getLogger(__name__)
#
#
# class ReleaseTemplateFormView(LoginRequiredMixin, View):
#     def get(self, request, release=None):
#         if not request.user.is_photographer:
#             return HttpResponseNotAllowed
#         request.session['model_release'] = release
#         templates = ReleaseTemplateChoiceForm(auto_id='temp_%s')
#         form = ReleaseTemplateForm()
#         use_form = ReleasePhotographerForm()  # TODO fix choices
#
#         return render(request, 'photo_app/release_template.html',
#                       {'form': form, 'templates': templates, 'use_form': use_form, 'release': release})
#
#     def post(self, request, release=None):
#         logging.debug(release)
#         if not request.user.is_photographer:
#             return HttpResponseNotAllowed
#         if release is not None:
#             instance = get_object_or_404(ReleaseTemplate, pk=release)
#         else:
#             instance = None
#             release = 0
#         logging.debug(instance)
#         form = ReleaseTemplateForm(request.POST, request.FILES, instance=instance, auto_id='temp_%s')
#         if form.is_valid():
#             logging.debug(form.cleaned_data)
#             form.save()
#
#         else:
#             logging.debug(form.errors)
#         templates = ReleaseTemplateChoiceForm()
#         return render(request, 'photo_app/release_template.html',
#                       {'form': form, 'templates': templates, 'release': release})
#
#
# class ReleaseTemplateView(LoginRequiredMixin, View):
#     model = {'first_name': 'MODEL', 'last_name': '', 'street': 'STREET', 'city': 'CITY', 'state': 'STATE',
#              'post_code': 'ZIP', 'nickname': 'NICKNAME', 'phone': 'PHONE', 'email': 'EMAIL'}
#
#     def dict_from_release(self, request, release):
#         mr = get_object_or_404(Release, pk=release)
#         d = {'photographer': self.user_dict(mr.photographer),
#              'date': mr.shoot_date,
#              'is_mature': mr.is_mature,
#              'model': self.model,
#              'use_full_name': mr.use_full_name,
#              'use_first_name': mr.use_first_name,
#              'use_nickname': mr.use_nickname,
#              'compensation': mr.compensation,
#              }
#         if request.user.id == mr.photo_model.id or (request.user.id == mr.photographer.id and mr.state is not None):
#             d['model'] = self.user_dict(mr.photo_model)
#         return d
#
#     def get(self, request, template):
#         # check to see if we are working on a release
#         release = request.session.get('model_release', None)
#         if release is None:
#             if not request.user.is_photographer:
#                 return HttpResponseNotAllowed
#             d = {'photographer': request.user, 'date': 'DATE', 'is_mature': True,
#                  'model': self.model, 'use_full_name': True, 'use_first_name': True, 'use_nickname': True,
#                  'compensation': '$$$'}
#         else:
#             d = self.dict_from_release(request, release)
#
#         rt = get_object_or_404(ReleaseTemplate, pk=template)
#         return HttpResponse(render(request, f'photo_app/release/{rt.file}.html', d))
#
#     def post(self, request, template):
#         def get_bool(par, request=request):
#             b = request.POST.get(par, ['true']),
#             logging.debug(b[0])
#             if b[0] == 'true':
#                 return True
#             return False
#         # check to see if we are working on a release
#         release = request.session.get('model_release', None)
#         if release is None:
#             if not request.user.is_photographer:
#                 return HttpResponseNotAllowed
#
#             d = {'photographer': request.user,
#                  'date': request.POST.get('date', 'DATE'),
#                  'is_mature': get_bool('is_mature'),
#                  'model': self.model,
#                  'use_full_name': get_bool('use_full_name'),
#                  'use_first_name': get_bool('use_first_name'),
#                  'use_nickname': get_bool('use_nickname'),
#                  'compensation': request.POST.get('compensation', '$$$'),
#                  }
#         else:
#             d = self.dict_from_release(request, release)
#         d['use_full_name'] = get_bool('use_full_name')
#         d['use_first_name'] = get_bool('use_first_name')
#         d['use_nickname'] = get_bool('use_nickname')
#         logging.debug(d)
#         rt = get_object_or_404(ReleaseTemplate, pk=template)
#         return HttpResponse(render(request, f'photo_app/release/{rt.file}.html', d))
#
#     def user_dict(self, user):
#         d = {'first_name': user.first_name, 'last_name': user.last_name, 'street': user.street, 'city': user.city,
#              'state': user.state, 'post_code': user.post_code, 'nickname': user.nickname, 'phone': user.phone,
#              'email': user.email}
#         return d
