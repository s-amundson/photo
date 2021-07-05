from django.forms import TextInput, ModelForm, DateField, IntegerField, ChoiceField

from ..models import Images, PhotoModel


class ImageForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Images
        fields = ['image', 'gallery']

