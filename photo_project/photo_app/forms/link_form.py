from django.forms import ModelForm

from ..models import LinkCategory, Links

from django import forms

# iterable
CHOICES = (
    ('website', "Website"),
    ("model_profile", "Model Profile"),
    ("social", "Social"),
)


class LinkForm(ModelForm):
    id = forms.CharField(required=False)
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        lc = LinkCategory.objects.all()
        choices = []
        for c in lc:
            choices.append((c.id, c.category))
        self.fields['category'].choices = choices
        self.fields['category'].widget.attrs.update({'class': 'form-control m-2'})
        self.fields['url'].widget.attrs.update({'class': 'form-control m-2', 'placeholder': "https://example.example.com"})
        self.fields['id'].widget = forms.HiddenInput()
    # https://rose.facebook.example.com {'placeholder': 'First Name'}

    class Meta:
        model = Links
        fields = ['category', 'id', 'url']
