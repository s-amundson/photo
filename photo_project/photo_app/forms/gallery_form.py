from django.forms import TextInput, ModelForm, DateField, IntegerField, ChoiceField

from ..models import Gallery, PhotoModel


class GalleryForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['photo_model'] = ChoiceField(required=False)
        self.fields['public_date'] = DateField(required=False)


    class Meta:
        model = Gallery
        exclude = ['owner']
