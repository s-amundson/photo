from django.forms import ModelForm

from ..models import Images


class ImageForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.Meta.optional_fields:
            self.fields[f].required = False

    class Meta:
        model = Images
        required_fields = ['image', 'privacy_level']
        optional_fields = ['raw_image']
        fields = required_fields + optional_fields

