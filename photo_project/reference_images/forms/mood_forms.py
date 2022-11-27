from src import MyModelForm
from ..models import Mood, MoodImage
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


class MoodForm(MyModelForm):

    class Meta(MyModelForm.Meta):
        model = Mood
        required_fields = ['mood_image']
        read_fields = []
        optional_fields = ['is_public']
        fields = required_fields + read_fields + optional_fields

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['is_public'].widget.attrs.update({'class': 'm-2'})


class MoodImageForm(MyModelForm):

    class Meta(MyModelForm.Meta):
        model = MoodImage
        required_fields = []
        read_fields = []
        optional_fields = ['comment', 'image', 'reference_image']
        fields = required_fields + read_fields + optional_fields
