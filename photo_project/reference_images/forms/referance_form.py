from django import forms
from ..models import Reference
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class ReferenceForm(forms.ModelForm):

    class Meta:
        model = Reference
        required_fields = ['category', 'image', 'link']
        read_fields = []
        optional_fields = ['active', 'is_model_mayhem', 'note']
        fields = required_fields + read_fields + optional_fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.Meta.optional_fields:
            self.fields[f].required = False
            # self.fields[f].widget.attrs.update({'class': 'form-control m-2'})
