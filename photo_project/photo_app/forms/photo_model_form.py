from django.forms import TextInput, ModelForm, DateField, IntegerField, ChoiceField, CharField

from ..models import Images, PhotoModel


class PhotoModelForm(ModelForm):
    first_name = CharField()
    last_name = CharField()
    # dob = DateField(error_messages={'invalid': "Enter a valid date in YYYY-MM-DD format"})

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = PhotoModel
        fields = ['first_name', 'last_name', 'dob', 'city', 'post_code', 'phone', 'state', 'street']
        widgets = {'first_name': TextInput(attrs={'placeholder': 'First Name', 'autocomplete': 'off',
                                                  'class': "form-control m-2"}),
                   'last_name': TextInput(attrs={'placeholder': 'Last Name', 'autocomplete': 'off',
                                                 'class': "form-control m-2"}),
                   'dob': TextInput(attrs={'placeholder': 'Date of Birth YYYY-MM-DD', 'autocomplete': 'off',
                                                 'class': 'form-control m-2',
                                                 'data-error-msg': "Please enter date in format YYYY-MM-DD"}),
                   }
