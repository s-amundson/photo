from django.forms import ModelForm, ClearableFileInput

from ..models import Images, ImageComment
# Get an instance of a logger
import logging
logger = logging.getLogger(__name__)


class ImageCommentForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.Meta.required_fields:
            self.fields[f].widget.attrs.update({'class': 'form-control m-2'})
        for f in self.Meta.hidden_fields:
            logging.warning(f)
            self.fields[f].required = False
            self.fields[f].widget.attrs.update({'class': 'form-control m-2', 'style': 'display:none'})


    class Meta:
        model = ImageComment
        hidden_fields = ['image', 'privacy_level', 'user']
        required_fields = ['comment']
        fields = required_fields + hidden_fields


class ImageForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.Meta.optional_fields:
            self.fields[f].required = False
        self.fields['image'].widget.attrs.update({'multiple': True})

    class Meta:
        model = Images
        required_fields = ['image', 'privacy_level']
        optional_fields = ['raw_image']
        fields = required_fields + optional_fields


class ImageUpdateForm(ImageForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Images
        required_fields = []
        optional_fields = ['raw_image', 'image', 'privacy_level']
        fields = required_fields + optional_fields
