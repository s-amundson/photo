from django.forms import ModelForm, DateField, ChoiceField, TextInput

from ..models import Gallery, User


class GalleryForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['public_date'] = DateField(required=False)

    class Meta:
        model = Gallery
        exclude = ['owner', 'photo_model']
        widgets = {'name': TextInput(attrs={'placeholder': 'Gallery Name', 'autocomplete': 'off',
                                            'class': "form-control m-2 member-required"}),
                   'public_date': TextInput(attrs={'placeholder': 'Date of Birth YYYY-MM-DD', 'autocomplete': 'off',
                                           'class': 'form-control m-2 member-required',
                                           'data-error-msg': "Please enter date in format YYYY-MM-DD"}),
                   'shoot_date': TextInput(attrs={'placeholder': 'Date of Birth YYYY-MM-DD', 'autocomplete': 'off',
                                           'class': 'form-control m-2 member-required',
                                           'data-error-msg': "Please enter date in format YYYY-MM-DD"}),
                   }

    # display_image
    # is_mature
    # is_public
    # photographer
    # shoot_date


class GalleryCreateForm(GalleryForm):
    class Meta(GalleryForm.Meta):
        exclude = ['display_image',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)