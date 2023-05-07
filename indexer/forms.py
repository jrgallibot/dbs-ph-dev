from django.forms import ModelForm
from .models import IndexApi,Website, Sitemap
from ckeditor.widgets import CKEditorWidget
from django import forms
class IndexerForm(ModelForm):
    class Meta:
        model = IndexApi
        fields = ['email', 'indexApi']

class WebsiteForm(ModelForm):
    class Meta:
        model = Website
        fields = ['website', 'pages']

class SitemapForm(ModelForm):
    results = forms.CharField(widget=CKEditorWidget())
    class Meta:
        model = Sitemap
        fields = ['website', 'results']