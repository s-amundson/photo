from django import forms
from ..models import Category


class CategoryForm(forms.ModelForm):

    class Meta:
        model = Category
        required_fields = ['title']
        optional_fields = []
        fields = optional_fields + required_fields
