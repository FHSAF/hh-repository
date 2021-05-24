from django import froms
from django.forms import widgets
from .models import Site

class SiteFrom(forms.ModelForm):
    class Meta:
        model = Site
        exclude = ('created_at',)

        widgets = {
            'url': forms.URLInput(attrs={'class': 'form-control',   'placeholder': 'Enter the website url'}),
            'name': forms.TextInput(attrs={'class': 'form-control',   'placeholder': 'Enter the website url'})
        }