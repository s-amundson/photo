from allauth.account.models import EmailAddress
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

import logging

logger = logging.getLogger(__name__)


class EmailMessage(EmailMultiAlternatives):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.from_email = settings.DEFAULT_FROM_EMAIL
        self.test_emails = ["EmilyNConlan@einrot.com", "RosalvaAHall@superrito.com", "CharlesNWells@einrot.com",
                            "RicardoRHoyt@jourrapide.com", "RicardoRHoyt@Ricardo.com"]

    def get_email_address(self, user):
        if settings.EMAIL_DEBUG:
            self.to = settings.EMAIL_DEBUG_ADDRESSES
        else:
            self.to = [EmailAddress.objects.get_primary(user)]
            if self.to in self.test_emails:
                self.to = settings.EMAIL_DEBUG_ADDRESSES

    def release_modified(self, user, release):
        """ Notifies model of a release just created. """

        self.get_email_address(user)
        logging.debug(self.to)

        self.subject = 'Updated Model release'
        d = {'name': user.first_name, 'release': release}
        self.body = get_template('photo_app/email/release_update_email.txt').render(d)
        self.attach_alternative(get_template('photo_app/email/release_update_email.html').render(d), 'text/html')
        self.send()

    def release_notification(self, user, release):
        """ Notifies model of a release just created. """

        self.get_email_address(user)
        logging.debug(self.to)

        self.subject = 'Pending Model release'
        d = {'name': user.first_name, 'release': release}
        self.body = get_template('photo_app/email/release_notification_email.txt').render(d)
        self.attach_alternative(get_template('photo_app/email/release_notification_email.html').render(d), 'text/html')
        self.send()
    # def refund_email(self, user, donation=False):
    #     self.get_email_address(user)
    #     d = {'name': user.first_name, 'donation': donation}
    #     self.subject = 'Woodley Park Archers Refund Confirmation'
    #     self.body = get_template('student_app/email/refund_email.txt').render(d)
    #     self.attach_alternative(get_template('student_app/email/refund_email.html').render(d), 'text/html')
    #     self.send()

    # def release_email(self, registration, pdf):
    #     cr = ClassRegistration.objects.get(pk=registration)
    #     users = cr.student.student_family.user.all()
    #     logging.debug(users)
    #     self.get_email_address(users[0])
    #     # TODO set to student if student is user.
    #     self.subject = ""
