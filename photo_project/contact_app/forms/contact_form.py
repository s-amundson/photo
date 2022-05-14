from django.forms import ModelForm
from ..models import Contact
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class ContactForm(ModelForm):

    class Meta:
        model = Contact
        required_fields = []
        read_fields = []
        optional_fields = ['first_name', 'last_name', 'email', 'phone', 'is_model', 'score', 'user']
        fields = required_fields + read_fields + optional_fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields['public_date'] = DateField(required=False)
        for f in self.Meta.optional_fields:
            self.fields[f].required = False
