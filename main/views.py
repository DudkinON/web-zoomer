from __future__ import unicode_literals

from django.conf import settings
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect, JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils import translation
from django.utils.translation import ugettext_lazy as _, LANGUAGE_SESSION_KEY
from django.utils.translation import get_language
from django.contrib.postgres.search import SearchVector
from django.db import connection
from django.contrib import messages

from re import findall, compile

from blog.models import Article, ArticleTag as Tag, Bookmarks
from main.models import Pages, Message
from main.forms import ContactForm
from web_zoomer_com.settings import AMOUNT_SEARCH_RESULT

app_name = 'main'


def home(request):
    """The home page

    :param request:
    :return:
    """
    args = dict()

    # get articles list
    args['articles'] = Article.objects.filter(
        is_active=True, language=get_language()).order_by(
        "-created")

    # define bookmarks list with articles ids
    if 'uid' in request.session:
        with connection.cursor() as c:
            c.execute("SELECT article_id FROM blog_bookmarks "
                      "WHERE reader_id=%s", [int(request.session['uid'])])
            bookmarks = [item[0] for item in c.fetchall()]
        args['bookmarks'] = bookmarks
    else:
        args['bookmarks'] = []

    # get csrf token
    csrf = str(get_token(request))

    if 'bookmark' in request.POST:

        if 'uid' not in request.session:
            return redirect(reverse('users:login'))
        print(request.POST, csrf)
        article_id = int(request.POST['article_id'])
        print(type(request.POST['bookmark']))
        if request.POST['bookmark'] == '1':
            print(request.POST['bookmark'], 'if')
            Bookmarks.objects.get_or_create(
                reader_id=request.session['uid'],
                article_id=article_id
            )
        else:
            print(request.POST['bookmark'], 'else')
            with connection.cursor() as c:
                c.execute("DELETE FROM blog_bookmarks "
                          "WHERE reader_id=%s AND article_id=%s",
                          [request.session['uid'], article_id])

        # json preparation
        json_response_prepare = {
            'csrf': csrf,
            'bookmark': int(request.POST['bookmark'])
        }
        return JsonResponse(dict(json_response_prepare))

    return render(request, 'main/home.html', args)


def about(request):
    """The about us page

    :param request:
    :return:
    """
    args = dict()
    args['about'] = Pages.objects.filter(title='About us').first() or None
    return render(request, 'main/about.html', args)


def contacts(request):
    """The contact page

    :param request:
    :return:
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
    :return:
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
    """The view for search

    :param request:
    :return:
    """
    args = dict()
    pattern = r"[а-я\w\d]+"
    comp = compile(pattern)
    if 'q' in request.GET:
        query = comp.findall(request.GET['q'].lower())
        q = ' '.join(query)

        results = Article.objects.annotate(
            search=SearchVector('text', 'title'),
        ).filter(search=q).order_by("-created").all()

    else:
        results = []

    # Pagination
    paginator = Paginator(results, AMOUNT_SEARCH_RESULT)
    if 'page' in request.GET:
        page = request.GET.get('page')
    else:
        page = 1
    print(page)
    try:
        args['search_results'] = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        args['search_results'] = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        args['search_results'] = paginator.page(paginator.num_pages)
    return render(request, 'main/search.html', args)
