from django.forms import ModelForm, SelectDateWidget
from django.utils.datetime_safe import date
from ..models import User
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class ProfileForm(ModelForm):

    class Meta:
        model = User
        required_fields = ['first_name', 'last_name', 'phone', 'street', 'city', 'state', 'post_code']
        read_fields = []
        optional_fields = ['is_model', 'dob', 'nickname']
        fields = required_fields + read_fields + optional_fields


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['dob'].widget = SelectDateWidget(years=range(date.today().year, date.today().year - 100, -1))
        for f in self.Meta.required_fields:
            self.fields[f].widget.attrs.update({'class': 'form-control m-2'})
        for f in self.Meta.optional_fields:
            self.fields[f].required = False
            self.fields[f].widget.attrs.update({'class': 'form-control m-2'})

        self.fields['dob'].label = "Date of Birth"
        self.fields['is_model'].label = "I am a Model"
        self.fields['is_model'].widget.attrs.update({'class': 'm-2'})
