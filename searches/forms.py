from django.forms import ModelForm
from .models import Search


class SearchForm(ModelForm):
    class Meta:
        model = Search
        fields = ("name", "url", "phrase", "date_found")
