from django.forms import ModelForm, TextInput, SelectDateWidget
from django.utils import timezone
from ..models import Gallery, Release, User
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class GalleryForm(ModelForm):

    class Meta:
        model = Gallery
        required_fields = ['name']
        read_fields = []
        optional_fields = ['display_image', 'is_mature', 'release', 'public_date', 'talent', 'photographer',
                           'privacy_level', 'shoot_date', 'description' ]
        fields = required_fields + read_fields + optional_fields

        # exclude = ['owner', 'photo_model']
        widgets = {'name': TextInput(attrs={'placeholder': 'Gallery Name', 'autocomplete': 'off',
                                            'class': "form-control m-2 member-required"}),
                   'public_date': SelectDateWidget(attrs={'autocomplete': 'off', 'class': 'form-control m-2'}),
                   'shoot_date': SelectDateWidget(attrs={'autocomplete': 'off', 'class': 'form-control m-2'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for f in self.Meta.optional_fields:
            self.fields[f].required = False

        if self.instance.id:
            self.fields['display_image'].queryset = self.instance.images_set.filter(privacy_level='public')
        else:
            self.fields['display_image'].queryset = None
        self.fields['release'].queryset = Release.objects.all().order_by('shoot_date')
        self.fields['photographer'].queryset = User.objects.filter(is_photographer=True)
        self.fields['public_date'].initial = timezone.datetime.today()
        self.fields['shoot_date'].initial = timezone.datetime.today()

