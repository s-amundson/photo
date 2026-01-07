from django.forms import ModelForm, SelectDateWidget, CheckboxInput
from django.utils import timezone
from ..models import User
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)

class MyCheckbox(CheckboxInput):
    def __init__(self, attrs=None):
        # Use slightly better defaults than HTML's 20x2 box
        default_attrs = {"class": "m-2"}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
class ProfileForm(ModelForm):

    class Meta:
        model = User
        required_fields = ['first_name', 'last_name', 'phone', 'street', 'city', 'state', 'post_code']
        read_fields = []
        optional_fields = ['is_model', 'dob', 'nickname']
        fields = required_fields + read_fields + optional_fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        d = timezone.datetime.today()
        self.fields['dob'].widget = SelectDateWidget(years=range(d.year, d.year - 100, -1))
        for f in self.Meta.required_fields:
            self.fields[f].widget.attrs.update({'class': 'form-control m-2'})
        for f in self.Meta.optional_fields:
            self.fields[f].required = False
            self.fields[f].widget.attrs.update({'class': 'form-control m-2'})

        self.fields['dob'].label = "Date of Birth"
        self.fields['is_model'].label = "I am a Model"
        self.fields['is_model'].widget.attrs.update({'class': 'form-check-input'})
