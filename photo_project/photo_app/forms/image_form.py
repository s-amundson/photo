from django.forms import ModelForm

from ..models import Images


class ImageForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Images
        fields = ['image', 'privacy_level']

