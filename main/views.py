from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.utils import translation
from blog.models import Article, ArticleTag as Tag
from main.models import Pages, Message
from main.forms import ContactForm
from django.utils.translation import ugettext_lazy as _, LANGUAGE_SESSION_KEY
from re import findall, compile
from django.contrib import messages

app_name = 'main'


def home(request):
    """The home page

    :param request:
    :return class:
    """
    context = dict()
    context['articles'] = Article.objects.filter(is_active=True).order_by(
        "-created")[:3]

    return render(request, 'main/home.html', context)


def about(request):
    """The about us page

    :param request:
    :return class:
    """
    context = dict()
    context['about'] = Pages.objects.filter(title='About us').first() or None
    return render(request, 'main/about.html', context)


def contacts(request):
    """The contact page

    :param request:
    :return class:
    """
    args = dict()
    args['title'] = _('Contacts')

    if request.method == 'POST':
        form = ContactForm(request.POST)
        args['form'] = form
        if form.is_valid():
            message = Message(email=form.cleaned_data['email'],
                              username=form.cleaned_data['username'],
                              title=form.cleaned_data['title'],
                              text=form.cleaned_data['text'])
            messages.info(request, _("Your message was sent successfully!"))
            message.save()
            return redirect('/')
        else:
            # print('errors: ', form.errors.as_data())
            return render(request, 'main/contacts.html', args)

    args['form'] = ContactForm(None)
    return render(request, 'main/contacts.html', args)


def select_lang(request, lang):
    """Switch user language by lang

    :param request:
    :param lang:
    :return class:
    """
    go_next = request.META.get('HTTP_REFERER', '/')
    response = HttpResponseRedirect(go_next)
    if lang and translation.check_for_language(lang):
        if hasattr(request, 'session'):
            request.session[LANGUAGE_SESSION_KEY] = lang
        else:
            response.set_cookie(settings.LANGUAGE_COOKIE_NAME, lang)
        translation.activate(lang)
    return response


def search(request):
    """The view for search, (unfinished)

    :param request:
    :return class:
    """
    args = dict()
    q = ''
    pattern = r'([a-zA-Z0-9]+)'
    comp = compile(pattern=pattern)
    query = findall(comp, request.GET['q'])
    for word in query:
        q += '{} '.format(word)
    q = q.rstrip()
    results_title = Article.objects.filter(title=q).all() or None
    results_text = Article.objects.filter(text=q).all() or None
    args['title'] = _('Search results')
    args['results'] = [results_title, results_text]
    return render(request, 'main/search.html', args)
