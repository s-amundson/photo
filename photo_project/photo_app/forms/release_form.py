from django.forms import ModelForm, BooleanField, CharField, HiddenInput, SelectDateWidget
import os
import base64
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import Paragraph, Frame, Image, Spacer
from reportlab.lib.pagesizes import letter

from django.core.files.base import File
from django.template.loader import get_template

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
        # self.fields['shoot_date'].widget = SelectDateWidget()
        self.signature = False
        self.empty_sig = 'data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAC2AX4DASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAAECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKRobHBCSMzUvAVYnLRChYkNOEl8RcYGRomJygpKjU2Nzg5OkNERUZHSElKU1RVVldYWVpjZGVmZ2hpanN0dXZ3eHl6goOEhYaHiImKkpOUlZaXmJmaoqOkpaanqKmqsrO0tba3uLm6wsPExcbHyMnK0tPU1dbX2Nna4uPk5ebn6Onq8vP09fb3+Pn6/9oADAMBAAIRAxEAPwD6pooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigAooooAKKKKACiiigD//Z'
        logging.debug(self.instance)

    def make_signature(self, fn, signee):
        image_b64 = self.cleaned_data[signee]
        img_format, imgstr = image_b64.split(';base64,')
        ext = img_format.split('/')[-1]
        with open('img.jpg', 'wb') as f:
            f.write(base64.b64decode(imgstr))
        return File(open('img.jpg', 'rb'), name=f'{fn}.jpg')

    def make_pdf(self):
        styles = getSampleStyleSheet()

        story = [Paragraph('Model Release', styles['Title'])]
        logging.debug(self.instance)
        template = get_template(f'photo_app/release/{self.instance.template.file}.txt').render(
            {'release': self.instance})
        template = template.split('\n')
        for line in template:
            if len(line):
                story.append(Paragraph(line, styles['Normal']))
            else:
                story.append(Spacer(1, 0.2 * inch))

        story.append(Paragraph("Model Signature:", styles['Normal']))
        talent_sig = Image(self.instance.talent_signature.file, width=3 * inch, height=1 * inch, hAlign='LEFT')
        story.append(talent_sig)
        story.append(Paragraph(f'Date: {self.instance.talent_signature_date}', styles['Normal']))
        story.append(Spacer(1, 0.2 * inch))
        story.append(Paragraph("Photographer Signature:", styles['Normal']))
        photo_sig = Image(self.instance.photographer_signature.file, width=3 * inch, height=1 * inch, hAlign='LEFT')
        story.append(photo_sig)
        story.append(Paragraph(f'Date: {self.instance.photographer_signature_date}', styles['Normal']))
        logging.debug(len(story))
        c = Canvas('mydoc.pdf', pagesize=letter)
        while len(story) > 0:
            f = Frame(inch / 2, inch, 7 * inch, 9 * inch, showBoundary=0)
            f.addFromList(story, c)
            c.showPage()
        c.save()
        self.instance.pdf = File(open('mydoc.pdf', 'rb'), name=f'{self.instance.id}.pdf')
        self.instance.save()

        # with open(os.path.join(settings.BASE_DIR, 'program_app', 'templates', 'program_app', 'awrl.txt'), 'r') as f:
        #     story.append(Paragraph(f.readline(), styles['Normal']))
        #     story.append(Spacer(1, 0.2 * inch))
        #     story.append(Paragraph(f.readline(), styles['Normal']))
        #     story.append(Spacer(1, 0.1 * inch))
        #     for line in f.readlines():
        #         story.append(Paragraph(line, styles['Bullet']))
        #         story.append(Spacer(1, 0.1 * inch))
        # story.append(Paragraph("Student:", styles['Normal']))
        # story.append(
        #     Paragraph(f'&nbsp;&nbsp;&nbsp;&nbsp;{self.student.first_name} {self.student.last_name}', styles['Normal']))
        # story.append(Paragraph(f'&nbsp;&nbsp;&nbsp;&nbsp;{sf.street}', styles['Normal']))
        # story.append(Paragraph(f'&nbsp;&nbsp;&nbsp;&nbsp;{sf.city} {sf.state} {sf.post_code}', styles['Normal']))
        #
        # new_sig = Image('img.jpg', width=3 * inch, height=1 * inch, hAlign='LEFT')
        # story.append(new_sig)
        # name = f"{self.cleaned_data['sig_first_name']} {self.cleaned_data['sig_last_name']}"
        # story.append(Paragraph(f"Signed By {name} on Date: {timezone.localtime(timezone.now()).date()}"))
        # c = Canvas('mydoc.pdf')
        # f = Frame(inch / 2, inch, 7 * inch, 9 * inch, showBoundary=1)
        # f.addFromList(story, c)
        # c.save()
        # fn = f'{self.student.last_name}_{self.student.first_name}'
        # self.student.signature = File(open('img.jpg', 'rb'), name=f'{fn}.jpg')
        # self.student.signature_pdf = File(open('mydoc.pdf', 'rb'), name=f'{fn}.pdf')


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
        self.fields['talent_signature'].widget.attrs.update({'class': 'signature'})
        self.fields['use_first_name'].label = f'Photographer may use my first name of ' \
                                              f'"{self.instance.talent.first_name}" in connection with the photographs'
        self.fields['use_full_name'].label = f'Photographer may use my full name of ' \
                                             f'"{self.instance.talent.first_name} {self.instance.talent.last_name}" ' \
                                             f'in connection with the photographs'
        if self.instance.talent.nickname is None:
            self.fields.pop('use_nickname')
        else:
            self.fields['use_nickname'].label = f'Photographer may use the name of ' \
                                            f'"{self.instance.talent.nickname}" in connection with the photographs'
        self.signature = True


class ReleasePhotographerForm(ReleaseForm):
    send_email = BooleanField()

    class Meta(ReleaseForm.Meta):
        exclude = ['talent_signature']
        required_fields = ['name', 'talent', 'shoot_date', 'template']
        read_fields = []
        optional_fields = ['compensation', 'is_mature', 'send_email', 'use_first_name', 'use_full_name', 'use_nickname', 'photographer_signature']
        fields = required_fields + read_fields + optional_fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        logging.warning(kwargs)
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
        self.fields['talent_signature'].required = False
        self.fields['photographer_signature'].widget.attrs.update({'class': 'signature'})
        logging.warning(self.instance.id)
        logging.warning(self.instance.id is None)
        self.signature = self.instance.id is not None


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
        # instance = kwargs.get('instance', None)
        # if instance is not None:
        #     for f in self.Meta.required_fields:
        #         self.fields[f].required = False
        # else:
        #     for f in self.Meta.required_fields:
        #         self.fields[f].required = True

        for f in self.Meta.hidden_fields:
            self.fields[f].required = False
            self.fields[f].widget.attrs.update({'class': 'form-control m-2', 'disabled': 'disabled'})
        self.signature = True

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
