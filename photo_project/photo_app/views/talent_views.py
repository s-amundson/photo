from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import ListView
from photo_app.models import Talent


class TalentCreateView(CreateView):
    model = Talent
    fields = ["talent", 'user']
    template_name = 'photo_app/form_as_p.html'
    success_url = reverse_lazy('photo_app:talent_list')


class TalentListView(ListView):
    model = Talent
    template_name = 'photo_app/talent_list.html'

    def get_queryset(self):
        queryset = self.model.objects.filter(user__is_active=True)
        return queryset.order_by('user__last_name')


class TalentUpdateView(UpdateView):
    model = Talent
    fields = ["talent", 'user']
    template_name = 'photo_app/form_as_p.html'
    success_url = reverse_lazy('photo_app:talent_list')
