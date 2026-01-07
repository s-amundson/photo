from django import forms
from src import MyModelForm
from ..models import Reference
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class ReferenceForm(MyModelForm):

    class Meta(MyModelForm.Meta):
        model = Reference
        required_fields = ['category', 'image']
        read_fields = []
        optional_fields = ['link', 'active', 'is_model_mayhem', 'note']
        fields = required_fields + read_fields + optional_fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['active'].widget.attrs.update({'class': 'm-2'})
        self.fields['is_model_mayhem'].widget.attrs.update({'class': 'm-2'})

