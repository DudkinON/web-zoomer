from django import forms
from .models import Article, ArticleImage
from wzwz_ru.settings import LANGUAGES


class ArticleForm(forms.Form):
    language = forms.ChoiceField(LANGUAGES)
    title = forms.CharField(max_length=255)
    description = forms.CharField(max_length=255)
    text = forms.CharField(max_length=5000, widget=forms.Textarea)

    class Meta:
        model = Article
        fields = ['language', 'description', 'title', 'text']


class ImageForm(forms.Form):
    image = forms.ImageField()

    class Meta:
        model = ArticleImage
        fields = ['image']


class EditArticleForm(forms.ModelForm):

    class Meta:
        model = Article
        fields = ['language', 'description', 'title', 'text']
