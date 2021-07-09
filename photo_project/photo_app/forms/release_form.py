from django.forms import ModelForm, DateField, ChoiceField

from ..models import Release, ReleaseTemplate


class ReleaseForm(ModelForm):

    class Meta:
        model = Release
        fields = ['file', 'name', 'model_signature', 'photographer', 'photographer_signature', 'photo_model',
                  'shoot_date', 'template']


class ReleaseModelForm(ReleaseForm):
    class Meta(ReleaseForm.Meta):
        read_fields = ['name', 'photographer', 'photo_model', 'shoot_date']
        optional_fields = ['model_signature']
        fields = read_fields + optional_fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for f in self.Mets.read_fields:
            self.fields[f].required = False
            self.fields[f].widget.attrs.update({'class': 'form-control m-2', 'readonly': 'readonly'})
        for f in self.Mets.optional_fields:
            self.fields[f].required = False


class ReleasePhotographerForm(ReleaseForm):

    class Meta(ReleaseForm.Meta):
        required_fields = ['name', 'photo_model', 'shoot_date', 'template']
        read_fields = ['model_signature']
        fields = required_fields + read_fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for f in self.Meta.required_fields:
            self.fields[f].required = True
            # self.fields[f].widget.attrs.update({'class': 'form-control m-2', 'required': 'required'})
        for f in self.Meta.read_fields:
            self.fields[f].required = False
            self.fields[f].widget.attrs.update({'class': 'form-control m-2', 'readonly': 'readonly'})


class ReleaseTemplateForm(ModelForm):

    class Meta:
        model = ReleaseTemplate
        fields = ['description', 'file']


class ReleaseTemplateChoiceForm(ReleaseTemplateForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        choices = []
        rt = ReleaseTemplate.objects.all()
        for t in rt:
            choices.append((t.id, f'{t.id} {t.description}'))
        self.fields['template_choice'] = ChoiceField(choices=choices)
