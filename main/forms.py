from django import forms
# from .models import Category as Cats


# def get_contact_categories():
#     contact_categories = Cats.objects.filter(is_active=True)
#     cats = tuple()
#     for i in contact_categories:
#         cats += (i.title,)
#     print(cats)
#     return cats


class ContactForm(forms.Form):
    username = forms.CharField(max_length=64)
    title = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=40)
    text = forms.CharField(max_length=250)
    contact_category = forms.ChoiceField(choices=('main', 'other'))
