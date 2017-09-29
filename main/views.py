from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.utils import translation
from blog.models import Blog, Category
from main.models import Pages, Category as Cats
from main.forms import ContactForm
from django.utils.translation import ugettext_lazy as _
from re import findall, compile
app_name = 'main'


def home(request):
    """The home page

    :param request:
    :return class:
    """
    context = dict()
    context['articles'] = Blog.objects.filter(is_active=True).order_by("-date")[:3]
    context['categories'] = Category.objects.filter(is_active=True) or None

    return render(request, 'main/index.html', context)


def about(request):
    """The about us page

    :param request:
    :return class:
    """
    context = dict()
    # context['about'] = Pages.objects.filter(title='About us').first()
    context['categories'] = Category.objects.filter(is_active=True)
    return render(request, 'main/about.html', context)


def contact(request):
    """The contact page

    :param request:
    :return class:
    """
    contact_categories = Cats.objects.all()
    context = dict()
    context['title'] = _('Contact')
    context['categs'] = contact_categories

    if request.method == 'POST' and request.POST.is_valid():
        form = ContactForm(request.POST)
        if form.is_valid():
            return render(request, 'main/contact.html', context)
    else:
        context['form'] = ContactForm()
        return render(request, 'main/contact.html', context)


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
            request.session['_language'] = lang
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
    print(q)
    results_title = Blog.objects.filter(title=q) or None
    results_text = Blog.objects.filter(text=q) or None
    args['title'] = _('Search results')
    args['results'] = [results_title, results_text]
    # args['results'] = results
    return render(request, 'main/search.html', args)
