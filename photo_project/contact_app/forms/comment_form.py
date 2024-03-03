from django.forms import ModelForm
from ..models import Comment
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class CommentForm(ModelForm):

    class Meta:
        model = Comment
        required_fields = ['comment']
        read_fields = ['person']
        hidden_fields = []
        optional_fields = []
        fields = required_fields + read_fields + optional_fields + hidden_fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for f in self.Meta.optional_fields:
            self.fields[f].required = False
        for f in self.Meta.hidden_fields:
            self.fields[f].required = False
            self.fields[f].widget.attrs.update({'class': 'form-control m-2', 'style': 'display:none'})
        for f in self.Meta.read_fields:
            self.fields[f].required = False
            self.fields[f].widget.attrs.update({'class': 'form-control m-2', 'readonly': 'readonly'})