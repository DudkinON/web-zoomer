from __future__ import unicode_literals

from django.middleware.csrf import get_token
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from django.db import connection
from re import findall, compile
from os import path, remove

from django.views import View

from wzwz_ru.settings import MEDIA_ROOT

from blog.forms import ArticleForm, ImageForm, EditArticleForm
from blog.models import Article, ArticleLikes, ArticleTag, ArticleImage
from users.models import User
from main.models import Languages
from wzwz_ru.settings import MEDIA_URL

app_name = 'blog'


def get_slug(title):
    """Generate slug by title

    :param title:
    :return string:
    """
    pattern = r'([a-zA-Zа-яА-Я0-9]+)'
    comp = compile(pattern=pattern)

    words = findall(comp, title.lower())
    return '_'.join(words)


def get_tags_list(string):
    """Generate tags list

    :param string:
    :return list:
    """
    pattern = r'([a-zA-Zа-яА-Я0-9]+)'
    comp = compile(pattern=pattern)
    return findall(comp, string.lower())


def articles(request):
    """View list of the last active articles

    :param request:
    :return:
    """
    args = dict()
    args['articles'] = Article.objects.filter(
        is_active=True).order_by("-created")[:10]
    args['title'] = _('Articles')

    return render(request, 'blog/index.html', args)


def article(request, slug):
    """view the article by slug

    :param request:
    :param slug:
    :return:
    """
    args = dict()
    current_article = get_object_or_404(Article, slug=slug)

    likes = ArticleLikes.objects.filter(
        like=True, article=current_article.id).all()
    dislikes = ArticleLikes.objects.filter(
        like=False, article=current_article.id).all()
    if request.session.test_cookie_worked():
        if str(current_article.id) not in request.COOKIES:
            request.session.delete_test_cookie()
            current_article.views += 1
            current_article.save(update_fields=['views'])
            response = HttpResponse('view')
            response.set_cookie(str(current_article.id), "True")

    if 'uid' in request.session:
        uid = request.session['uid']
    else:
        uid = None

    if request.method == 'POST':
        # print(request.POST)
        print(bool(int(request.POST['like'][0])))
        if 'uid' not in request.session:
            messages.error(request, _("Only registered users can vote"))
            return redirect(reverse('users:login'))
        else:
            try:
                current_like, _created = ArticleLikes.objects.get_or_create(
                    article=current_article,
                    user=User.objects.get(id=uid))
                current_like.like = bool(int(request.POST['like'][0]))
                current_like.save()
                json_response_prepare = {
                    'csrf': str(get_token(request)),
                    'likes': likes.count() or 0,
                    'dislikes': dislikes.count() or 0
                }
                return JsonResponse(json_response_prepare)
            except:
                pass
    current_user_like = ArticleLikes.objects.filter(
        article=current_article.id, user=uid).first() or None
    if current_user_like is not None:
        current_user_like = int(current_user_like.like)

    args['uid'] = uid
    args['likes'] = likes.count() or 0
    args['dislikes'] = dislikes.count() or 0
    args['articles'] = Article.objects.filter(
        is_active=True).order_by('views')[:4]
    args['current_user_like'] = current_user_like
    args['article'] = current_article
    args['published_stories'] = Article.objects.filter(
        author=current_article.author).all().count() or 0
    args['tags'] = current_article.tags.all()

    return render(request, 'blog/article.html', args)


def tag_sort(request, tag):
    """View articles by tag

    :param request:
    :param tag:
    :return:
    """
    args = dict()
    args['articles'] = ArticleTag.objects.get(tag=tag).article_set.all()
    return render(request, 'blog/tags.html', args)


def create_article(request):
    """Create new article

    :param request:
    :return:
    """
    args = dict()
    if 'uid' not in request.session:
        messages.error(request, _("Only registered users can write stories"))
        return redirect(reverse('users:login'))
    user = User.objects.get(id=request.session['uid'])
    form = ArticleForm(None)
    image = None
    image_form = ImageForm(None)
    args['form'] = form
    args['image_form'] = image_form
    if request.method == 'POST':
        if 'upload_image' in request.POST:
            image_form = ImageForm(request.POST, request.FILES)
            args['image_form'] = image_form

            if image_form.is_valid():
                image = ArticleImage.objects.create(
                    image=image_form.cleaned_data['image'],
                    user=user
                )
                image.save()
                image = ArticleImage.objects.get(id=image.id)
                request.session['image'] = str(image.image)
            return render(request, 'blog/create.html', args)
        elif 'create' in request.POST:
            form = ArticleForm(request.POST)
            args['form'] = form
            if form.is_valid():
                new_article = Article.objects.create(
                    language=Languages.objects.get(
                        code=form.cleaned_data['language']),
                    image=ArticleImage.objects.get(
                        image=request.session['image']),
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    text=form.cleaned_data['text'],
                    author=user,
                    slug=get_slug(form.cleaned_data['title']),
                    is_active=False
                )
                new_article.save()
                request.session['article_id'] = int(new_article.id)

        elif 'finish' in request.POST:
            tags = request.POST['tags']
            current_article = Article.objects.get(
                id=request.session['article_id'])
            if len(tags) > 1:
                args['tags'] = tags
                tags_list = list()
                tags_tmp = get_tags_list(tags)
                for word in tags_tmp:
                    tags_list.append(ArticleTag.objects.get_or_create(
                        tag=word, language=Languages.objects.get(
                            code=current_article.language.code))[0])
                current_article.tags.add(*tags_list)
                current_article.save()
                del request.session['article_id']
                del request.session['image']
                messages.info(request, _("Your article was sent for review. "
                                         "You can edit article in your profile"
                                         "."))

                return redirect(reverse(
                    'users:profile', kwargs={'uid': request.session['uid']}))

            else:
                messages.error(request, _("Tag can't be empty"))
    if 'article_id' in request.session:
        args['temp_article'] = Article.objects.get(
            id=request.session['article_id']) or None
    return render(request, 'blog/create.html', args)


class EditArticle(View):
    template_name = 'blog/edit-article.html'
    args = None
    tags_list = list()

    def get(self, request, slug):
        """Response on get query

        :param request:
        :param slug:
        :return:
        """
        if 'uid' not in request.session:
            messages.error(request, _("Only registered users can edit stories"))
            return redirect(reverse('users:login'))

        current_article = get_object_or_404(Article, slug=slug)

        if int(current_article.author_id) != request.session['uid']:
            messages.error(request,
                           _("You don't have permission to edit this story"))
            return redirect(reverse('users:profile',
                                    kwargs={'uid': request.session['uid']}))

        user = User.objects.get(id=request.session['uid'])
        img_form = ImageForm(None)

        form = EditArticleForm(instance=current_article)
        self.args = dict()
        self.args['user'] = user
        self.args['article'] = current_article
        self.args['tags'] = current_article.tags.all()
        self.args['media'] = MEDIA_URL
        self.args['image'] = current_article.image.image
        self.args['form'] = form
        self.args['img_form'] = img_form

        return render(request, self.template_name, self.args)

    def post(self, request, slug):
        """Update article data

        :param request:
        :param slug:
        :return:
        """
        img_form = ImageForm(None)

        if 'uid' not in request.session:
            messages.error(request, _("Only registered users can edit stories"))
            return redirect(reverse('users:login'))
        user = User.objects.get(id=request.session['uid'])

        current_article = get_object_or_404(Article, slug=slug)
        form = EditArticleForm(instance=current_article)
        self.args = dict()
        self.args['img_form'] = img_form
        self.args['article'] = current_article
        self.args['tags'] = current_article.tags.all()
        self.args['media'] = MEDIA_URL
        self.args['image'] = current_article.image.image
        self.args['form'] = form

        if 'upload_image' in request.POST:
            # handler for edit image
            img_form = ImageForm(request.POST, request.FILES)
            self.args['img_form'] = img_form
            if img_form.is_valid():
                image = ArticleImage.objects.create(
                    image=img_form.cleaned_data['image'],
                    user=user
                )
                if path.isfile(MEDIA_ROOT + '/' + str(self.args['image'])):
                    remove(MEDIA_ROOT + '/' + str(self.args['image']))
                image.save()
                image_id = int(current_article.image.id)
                current_article.image = ArticleImage.objects.get(id=image.id)
                current_article.is_active = False
                current_article.save(update_fields=['image'])

                with connection.cursor() as c:
                    c.execute("DELETE FROM blog_articleimage "
                              "WHERE id=%s", [image_id])
                return redirect(reverse('blog:edit_article',
                                        kwargs={'slug': slug}))

        elif 'save' in request.POST:
            # handler for edit article
            article_title = str(current_article.title)
            form = EditArticleForm(request.POST, instance=current_article)
            self.args['form'] = form
            if form.is_valid():
                update_article = form.save(commit=False)

                # if title was changed change slug
                if article_title != form.cleaned_data['title']:
                    update_article.slug = get_slug(form.cleaned_data['title'])
                update_article.is_active = False
                update_article.save()
                return redirect(reverse('blog:edit_article',
                                        kwargs={'slug': slug}))
        elif 'tags' in request.POST:
            # handler for add tag POST query
            tags = request.POST['tags']

            if len(tags) > 1:
                # generate tags
                for word in get_tags_list(tags):
                    self.tags_list.append(ArticleTag.objects.get_or_create(
                        tag=word, language=Languages.objects.get(
                            code=current_article.language.code))[0])
                # add tags to article
                current_article.tags.add(*self.tags_list)
                current_article.save()
            else:
                messages.error(request,
                               _("You have to add minimum one tag"))

        elif 'remove_tag' in request.POST:
            # handler for remove tag (AJAX POST query)
            if request.POST['remove_tag'].isdigit():
                tag_id = int(request.POST['remove_tag'])
            else:
                messages.error(request, _("Tag not found"))
                return redirect(reverse('blog:edit_article',
                                        kwargs={'slug': slug}))
            art_id = int(current_article.id)

            with connection.cursor() as c:
                c.execute(
                    "SELECT id FROM public.blog_article_tags "
                    "WHERE article_id=%(aid)s AND articletag_id=%(tid)s",
                    {'aid': art_id, 'tid': tag_id})
                m2m = c.fetchone()[0]

            if m2m > 0:
                with connection.cursor() as c:
                    c.execute("DELETE FROM blog_article_tags "
                              "WHERE id=%s", [m2m])
                    c.execute(
                        """SELECT "blog_articletag"."id", 
                        "blog_articletag"."tag"
                        FROM "blog_articletag" INNER JOIN "blog_article_tags" 
                        ON ("blog_articletag"."id" = 
                        "blog_article_tags"."articletag_id") 
                        WHERE "blog_articletag"."is_active"=TRUE AND 
                        "blog_article_tags"."article_id"=%s""",
                        [art_id])
                    response = c.fetchall()
                    json_response_prepare = {
                        'csrf': str(get_token(request)),
                        'data': dict(response)
                    }
                return JsonResponse(dict(json_response_prepare))

        return render(request, self.template_name, self.args)


def delete_article(request, slug):
    """Delete an article

    :param request:
    :param slug:
    :return:
    """

    if 'uid' not in request.session:
        messages.error(request, _("Only registered users can delete stories"))
        return redirect(reverse('users:login'))

    current_article = get_object_or_404(Article, slug=slug)

    if int(current_article.author_id) != request.session['uid']:
        messages.error(request,
                       _("You don't have permission to delete this story"))
        return redirect(reverse('users:profile',
                                kwargs={'uid': request.session['uid']}))

    args = dict()
    args['media'] = MEDIA_URL
    args['article'] = current_article
    args['image'] = current_article.image.image

    if request.method == 'POST' and 'title' in request.POST:
        if request.POST['title'] == current_article.title:
            title = str(request.POST['title'])
            if path.isfile(MEDIA_ROOT + '/' + str(args['image'])):
                remove(MEDIA_ROOT + '/' + str(args['image']))
            current_article.delete()
            message = _("The story was deleted. Story name: ") + title
            messages.info(request, message)
            return redirect(reverse('users:profile',
                                    kwargs={'uid': request.session['uid']}))

    return render(request, 'blog/delete-article.html', args)
