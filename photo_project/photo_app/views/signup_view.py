from allauth.account.views import SignupView as ASV
from ipware import get_client_ip

import logging
logger = logging.getLogger(__name__)


class SignupView(ASV):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # self.request.session.pop('recaptcha_scores')
        score = self.request.session.get('recaptcha_score', 0)
        logging.warning(score)
        context['probably_human'] = score > 0.7
        return context

    # def get_form_kwargs(self):
    #     kwargs = super().get_form_kwargs()
    #     kwargs['client_ip'], kwargs['is_routable'] = get_client_ip(self.request)
    #     logging.warning(f"ip: {kwargs['client_ip']}, routable: {kwargs['is_routable']}")
    #     return kwargs
