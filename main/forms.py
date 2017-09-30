from django import forms
from .models import Message, Category as Cats


def get_contact_categories():
    """Return tuple of contact categories

    :return tuple:
    """
    contact_categories = Cats.objects.filter(is_active=True) or None
    cats = tuple()
    if contact_categories:
        for i in contact_categories.title:
            cats += (i.title,)
    return cats


class ContactForm(forms.Form):
    username = forms.CharField(max_length=64)
    title = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=40)
    text = forms.CharField(max_length=250)
    contact_category = forms.ChoiceField(choices=get_contact_categories())

    class Meta:
        model = Message
        fields = ['email', 'username', 'category', 'title', 'text']
