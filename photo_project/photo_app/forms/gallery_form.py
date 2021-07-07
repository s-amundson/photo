from django.forms import ModelForm, DateField, ChoiceField

from ..models import Gallery, User


class GalleryForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO search for user by email address
        self.fields['public_date'] = DateField(required=False)


    class Meta:
        model = Gallery
        exclude = ['owner', 'photo_model']
