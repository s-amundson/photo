from django.forms import ModelForm, BooleanField, ChoiceField, model_to_dict, CharField, HiddenInput
import os
import base64
from django.core.files.base import File

from ..models import Release, ReleaseTemplate

# Get an instance of a logger
import logging

logger = logging.getLogger(__name__)


class ReleaseForm(ModelForm):

    class Meta:
        model = Release
        fields = ['compensation', 'file', 'is_mature', 'name', 'photographer', 'talent', 'shoot_date', 'template',
                  'use_first_name', 'use_full_name', 'use_nickname', 'photographer_signature', 'talent_signature']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        rt = ReleaseTemplate.objects.all()
        choices = []
        for t in rt:
            choices.append((t.id, t.description))
        self.fields['template'].choices = choices
        self.fields['talent_signature'] = CharField(widget=HiddenInput())
        self.fields['photographer_signature'] = CharField(widget=HiddenInput())
        self.signature = False
        self.empty_sig = 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAC2AX4DASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD6pooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigD//Z'
        logging.debug(self.instance)

    # def make_signature(self, fn):
    #     image_b64 = self.cleaned_data['talent_signature']
    #     img_format, imgstr = image_b64.split(';base64,')
    #     ext = img_format.split('/')[-1]
    #     with open('img.jpg', 'wb') as f:
    #         f.write(base64.b64decode(imgstr))
    #     return File(open('img.jpg', 'rb'), name=f'{fn}.jpg')

    def make_pdf(self):
        logging.debug(self.instance)
        image_b64 = self.cleaned_data['photographer_signature']
        img_format, imgstr = image_b64.split(';base64,')

        ext = img_format.split('/')[-1]
        with open('psig.jpg', 'wb') as f:
            f.write(base64.b64decode(imgstr))


class ReleaseModelForm(ReleaseForm):

    class Meta(ReleaseForm.Meta):
        hidden_fields = ['template']
        read_fields = []
        exclude = ['compensation', 'file', 'name', 'photographer', 'talent', 'shoot_date', 'photographer_signature']
        optional_fields = ['use_first_name', 'use_full_name', 'use_nickname', 'talent_signature']
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
            self.fields[f].widget.attrs.update({'class': 'form-control m-2', 'disabled': 'disabled',
                                                'style': 'display:none'})
        self.fields['photographer_signature'].required = False
        self.fields['use_first_name'].label = f'Photographer may use my first name of ' \
                                              f'"{self.instance.talent.first_name}" in connection with the photographs'
        self.fields['use_full_name'].label = f'Photographer may use my full name of ' \
                                             f'"{self.instance.talent.first_name} {self.instance.talent.last_name}" ' \
                                             f'in connection with the photographs'
        self.fields['use_nickname'].label = f'Photographer may use the name of ' \
                                            f'"{self.instance.talent.nickname}" in connection with the photographs'
        self.signature = True


class ReleasePhotographerForm(ReleaseForm):
    send_email = BooleanField()

    class Meta(ReleaseForm.Meta):
        exclude = ['talent_signature', 'photographer_signature']
        required_fields = ['name', 'talent', 'shoot_date', 'template']
        read_fields = []
        optional_fields = ['compensation', 'is_mature', 'send_email', 'use_first_name', 'use_full_name', 'use_nickname']
        fields = required_fields + read_fields + optional_fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.debug(kwargs)
        # logging.debug(model_to_dict(kwargs['instance']))
        for f in self.Meta.required_fields:
            self.fields[f].required = True
        # for f in self.Meta.read_fields:
        #     self.fields[f].required = False
        #     self.fields[f].widget.attrs.update({'class': 'form-control m-2', 'readonly': 'readonly'})
        for f in self.Meta.optional_fields:
            self.fields[f].required = False
        for f in self.Meta.exclude:
            self.fields[f].required = False


class ReleaseSignedForm(ReleaseForm):
    send_email = BooleanField(required=False)

    class Meta(ReleaseForm.Meta):
        hidden_fields = ['template']
        required_fields = []
        exclude = ['compensation', 'name', 'photographer', 'talent', 'shoot_date', 'use_first_name',
                   'use_full_name', 'use_nickname', 'file']
        fields = required_fields + hidden_fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance', None)
        if instance is not None:
            for f in self.Meta.required_fields:
                self.fields[f].required = False
        else:
            for f in self.Meta.required_fields:
                self.fields[f].required = True

        for f in self.Meta.hidden_fields:
            self.fields[f].required = False
            self.fields[f].widget.attrs.update({'class': 'form-control m-2', 'disabled': 'disabled'})


class ReleaseTemplateForm(ModelForm):

    class Meta:
        model = ReleaseTemplate
        fields = ['description', 'file']


# class ReleaseTemplateChoiceForm(ReleaseTemplateForm):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         choices = []
#         rt = ReleaseTemplate.objects.all()
#         for t in rt:
#             choices.append((t.id, f'{t.id} {t.description}'))
#         self.fields['template_choice'] = ChoiceField(choices=choices)
