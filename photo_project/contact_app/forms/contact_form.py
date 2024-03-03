from django.forms import CharField, Form, ModelForm, TextInput
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
        self.has_instance = kwargs.get('instance', None)
        for f in self.Meta.optional_fields:
            self.fields[f].required = False


class ContactSearchForm(Form):
    first_name = CharField(widget=TextInput(attrs={'placeholder': 'First Name', 'autocomplete': 'off',
                                                   'class': "form-control m-2"}), required=False)
    last_name = CharField(widget=TextInput(attrs={'placeholder': 'Last Name', 'autocomplete': 'off',
                                                  'class': "form-control m-2"}), required=False)
