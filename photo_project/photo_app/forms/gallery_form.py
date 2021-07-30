from django.forms import ModelForm, DateField, ChoiceField, TextInput, CheckboxInput

from ..models import Gallery, User


class GalleryForm(ModelForm):

    class Meta:
        model = Gallery
        required_fields = ['name']
        read_fields = []
        optional_fields = ['display_image', 'is_mature', 'is_public', 'photo_model', 'public_date', 'photographer',
                           'shoot_date']
        fields = required_fields + read_fields + optional_fields

        # exclude = ['owner', 'photo_model']
        widgets = {'name': TextInput(attrs={'placeholder': 'Gallery Name', 'autocomplete': 'off',
                                            'class': "form-control m-2 member-required"}),
                   'public_date': TextInput(attrs={'placeholder': 'YYYY-MM-DD', 'autocomplete': 'off',
                                           'class': 'form-control m-2 member-required',
                                           'data-error-msg': "Please enter date in format YYYY-MM-DD"}),
                   'shoot_date': TextInput(attrs={'placeholder': 'YYYY-MM-DD', 'autocomplete': 'off',
                                           'class': 'form-control m-2 member-required',
                                           'data-error-msg': "Please enter date in format YYYY-MM-DD"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['public_date'] = DateField(required=False)
        for f in self.Meta.optional_fields:
            self.fields[f].required = False
        self.fields['photo_model'].choices = self.model_choices()
        self.fields['photographer'].choices = self.photographer_choices()

    def model_choices(self):
        pm = User.objects.filter(is_model=True)
        choices = []
        for m in pm:
            choices.append((m.id, f'{m.first_name} {m.last_name}'))
        return choices

    def photographer_choices(self):
        p = User.objects.filter(is_photographer=True)
        choices = []
        for m in p:
            choices.append((m.id, f'{m.first_name} {m.last_name}'))
        return choices
# 'display_image', 'is_mature', 'is_public', 'name', 'owner', 'photo_model', 'public_date', 'photographer', 'shoot_date'


class GalleryCreateForm(GalleryForm):
    class Meta(GalleryForm.Meta):
        required_fields = ['name']
        read_fields = []
        optional_fields = ['is_mature', 'is_public', 'photo_model', 'public_date', 'photographer',
                           'shoot_date']
        fields = required_fields + read_fields + optional_fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for f in self.Meta.optional_fields:
            self.fields[f].required = False
