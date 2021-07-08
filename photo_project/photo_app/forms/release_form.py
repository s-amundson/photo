from django.forms import ModelForm, DateField, ChoiceField

from ..models import Release, ReleaseTemplate


class ReleaseForm(ModelForm):

    class Meta:
        model = Release
        fields = ['file', 'name', 'model_signature', 'photographer', 'photographer_signature', 'photo_model',
                  'shoot_date', 'template']


class ReleaseModelForm(ReleaseForm):
    class Meta(ReleaseForm.Meta):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        read_fields = ['name', 'photographer', 'photographer_signature', 'photo_model',
                       'shoot_date']
        optional_fields = ['model_signature']
        for f in read_fields:
            self.fields[f].required = False
            self.fields[f].widget.attrs.update({'class': 'form-control m-2', 'readonly': 'readonly'})
        for f in optional_fields:
            self.fields[f].required = False
        self.Meta.fields = read_fields + optional_fields




class ReleasePhotographerForm(ReleaseForm):
    class Meta(ReleaseForm.Meta):
        pass

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        required_fields = ['name', 'photographer', 'photographer_signature', 'photo_model',
                       'shoot_date']
        optional_fields = ['model_signature']
        for f in required_fields:
            self.fields[f].required = False
            # self.fields[f].widget.attrs.update({'class': 'form-control m-2', 'required': 'required'})
        for f in optional_fields:
            self.fields[f].required = False
        self.Meta.fields = required_fields + optional_fields


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
