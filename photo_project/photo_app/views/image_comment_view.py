from django.contrib.auth.mixins import UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.shortcuts import get_object_or_404
from django.db.models import Q

from ..forms import ImageCommentForm
from ..models import Gallery, Images, ImageComment


# Get an instance of a logger
import logging
logger = logging.getLogger(__name__)


class ImageCommentView(UserPassesTestMixin, FormView):
    form_class = ImageCommentForm
    image = None
    template_name = 'photo_app/forms/image_comment.html'
    success_url = reverse_lazy('photo:index')

    def get_comments(self):
        comments = ImageComment.objects.filter(image=self.image).order_by('comment_date')
        if self.request.user.is_authenticated:
            if self.request.user.is_staff:
                return comments
            else:
                comments = comments.filter(Q(privacy_level='public') | Q(user=self.request.user))
        else:
            comments.filter(privacy_level='public')
        return comments

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.get_comments()
        context['comment_form'] = context.pop('form')
        context['image_id'] = self.image.id
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['initial'] = {'image': self.image, 'user': self.request.user}
        return kwargs

    def form_invalid(self, form):
        logging.warning(form.errors)
        return super().form_invalid(form)

    def form_valid(self, form):
        logging.warning(form.cleaned_data)
        comment = form.save()
        return super().form_valid(form)

    def test_func(self):
        if self.request.user.is_authenticated:
            logging.warning(self.request.POST)
            iid = self.kwargs.get('image_id', None)
            if iid is not None:
                self.image = get_object_or_404(Images, pk=iid)
                self.success_url = reverse_lazy('photo:image', kwargs={'image_id': self.image.id})
                return True
        return False
