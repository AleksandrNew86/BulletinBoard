from django import forms
from ckeditor.fields import RichTextField
from .models import Ad


class AdForm(forms.ModelForm):

    class Meta:
        model = Ad
        fields = ['category_ad', 'title_ad', 'content_ad']
        labels = {
            'category_ad': "Категория",
            'title_ad': 'Название',
            'content_ad': 'Содержание',
        }

