from django.forms import ModelForm, BooleanField, ChoiceField

from ..models import Release, ReleaseTemplate
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class ReleaseForm(ModelForm):

    class Meta:
        model = Release
        fields = ['compensation', 'file', 'is_mature', 'name', 'photographer', 'photo_model', 'shoot_date', 'template',
                  'use_first_name', 'use_full_name', 'use_nickname']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        rt = ReleaseTemplate.objects.all()
        choices = []
        for t in rt:
            choices.append((t.id, t.description))
        self.fields['template'].choices = choices


class ReleaseModelForm(ReleaseForm):
    agree = BooleanField(label="I agree with this release")
    class Meta(ReleaseForm.Meta):
        hidden_fields = ['template']
        read_fields = []
        exclude = ['compensation', 'file', 'name', 'photographer', 'photo_model', 'shoot_date']
        optional_fields = ['use_first_name', 'use_full_name', 'use_nickname', 'agree']
        fields = read_fields + optional_fields + hidden_fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # for f in self.Meta.read_fields:
        #     self.fields[f].required = False
        #     self.fields[f].widget.attrs.update({'class': 'form-control m-2', 'disabled': 'disabled'})
        for f in self.Meta.optional_fields:
            self.fields[f].required = False
        for f in self.Meta.hidden_fields:
            self.fields[f].required = False
            self.fields[f].widget.attrs.update({'class': 'form-control m-2', 'disabled': 'disabled'})


class ReleasePhotographerForm(ReleaseForm):
    send_email = BooleanField()

    class Meta(ReleaseForm.Meta):
        required_fields = ['name', 'photo_model', 'shoot_date', 'template']
        read_fields = []
        optional_fields = ['compensation', 'is_mature', 'send_email', 'use_first_name', 'use_full_name', 'use_nickname']
        fields = required_fields + read_fields + optional_fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.debug(kwargs)
        for f in self.Meta.required_fields:
            self.fields[f].required = True
        for f in self.Meta.read_fields:
            self.fields[f].required = False
            self.fields[f].widget.attrs.update({'class': 'form-control m-2', 'readonly': 'readonly'})
        for f in self.Meta.optional_fields:
            self.fields[f].required = False


class ReleaseSignedForm(ReleaseForm):
    send_email = BooleanField()

    class Meta(ReleaseForm.Meta):
        fields = ['file']


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
