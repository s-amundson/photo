from django.http import JsonResponse
from django.views.generic.edit import FormView
from django.urls import reverse_lazy
from ipware import get_client_ip

from ..forms import RecaptchaFormV3

import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class RecaptchaThreeView(FormView):
    form_class = RecaptchaFormV3
    template_name = 'recaptcha/recaptcha.html'
    success_url = reverse_lazy('photo_app:index')

    def form_invalid(self, form):
        logging.warning(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        client_ip, is_routable = get_client_ip(self.request)
        score = form.get_score(client_ip)
        if score is not None:
            self.request.session['recaptcha_score'] = score
        if self.request.META.get('HTTP_ACCEPT', '').find('application/json') >= 0:
            logging.warning('json response')
            return JsonResponse({'status': 'success'})
        self.success_url = form.cleaned_data['url']
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        return context
