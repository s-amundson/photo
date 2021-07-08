from django.forms import ModelForm, DateField, ChoiceField

from ..models import ReleaseTemplate


class ReleaseTemplateForm(ModelForm):

    class Meta:
        model = ReleaseTemplate
        fields = ['description', 'file']
