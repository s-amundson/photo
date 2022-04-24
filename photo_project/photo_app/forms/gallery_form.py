from django.forms import ModelForm, DateField, ChoiceField, TextInput, CheckboxInput, SelectDateWidget
from django.utils.datetime_safe import date
from ..models import Gallery, Release, User
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class GalleryForm(ModelForm):

    class Meta:
        model = Gallery
        required_fields = ['name']
        read_fields = []
        optional_fields = ['display_image', 'is_mature', 'release', 'public_date', 'photographer',
                           'privacy_level', 'shoot_date', 'description']
        fields = required_fields + read_fields + optional_fields

        # exclude = ['owner', 'photo_model']
        widgets = {'name': TextInput(attrs={'placeholder': 'Gallery Name', 'autocomplete': 'off',
                                            'class': "form-control m-2 member-required"}),
                   'public_date': SelectDateWidget(attrs={'autocomplete': 'off', 'class': 'form-control m-2'}),
                   'shoot_date': SelectDateWidget(attrs={'autocomplete': 'off', 'class': 'form-control m-2'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.fields['public_date'] = DateField(required=False)
        for f in self.Meta.optional_fields:
            self.fields[f].required = False
        self.fields['display_image'].queryset = self.instance.images_set.filter(privacy_level='public')
        self.fields['release'].choices = self.release_choices()
        self.fields['photographer'].choices = self.photographer_choices()
        self.fields['public_date'].initial = date.today()
        self.fields['shoot_date'].initial = date.today()

    def release_choices(self):
        pm = Release.objects.filter(state='complete')
        choices = []
        for m in pm:
            choices.append((m.id, m.shoot_date))
        return choices

    def photographer_choices(self):
        p = User.objects.filter(is_photographer=True)
        choices = []
        for m in p:
            choices.append((m.id, f'{m.first_name} {m.last_name}'))
        return choices
# 'display_image', 'is_mature', 'is_public', 'name', 'owner', 'photo_model', 'public_date', 'photographer', 'shoot_date'


# class GalleryCreateForm(GalleryForm):
#     class Meta(GalleryForm.Meta):
#         required_fields = ['name']
#         read_fields = []
#         optional_fields = ['is_mature', 'is_public', 'release', 'public_date', 'photographer',
#                            'shoot_date']
#         fields = required_fields + read_fields + optional_fields
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for f in self.Meta.optional_fields:
#             self.fields[f].required = False
