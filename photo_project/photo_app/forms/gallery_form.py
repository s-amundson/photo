from django.forms import ModelForm, DateField, ChoiceField

from ..models import Gallery, User


class GalleryForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # TODO search for user by email address
        # pm = User.objects.filter(is_model=True)
        # choices = [(None, "None")]
        # for m in pm:
        #     choices.append((m.id, f'{m.first_name} {m.last_name}'))
        # self.fields['photo_model'] = ChoiceField(required=False)
        self.fields['public_date'] = DateField(required=False)


    class Meta:
        model = Gallery
        exclude = ['owner']
