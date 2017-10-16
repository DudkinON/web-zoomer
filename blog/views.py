from __future__ import unicode_literals
from django.middleware.csrf import get_token
from django.http import JsonResponse
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


def articles(request):
    args = dict()
    args['articles'] = Article.objects.filter(
        is_active=True).order_by("-created")[:3]
    args['title'] = 'Articles'
    args['page'] = 'Blog page'
    return render(request, 'blog/index.html', args)


def article(request, slug):
    args = dict()
    current_article = get_object_or_404(Article, slug=slug)
    article_model = ArticleLikes.objects

    if 'viewed' not in request.session:
        request.session['viewed'] = True
        current_article.views += 1
        current_article.save(update_fields=['views'])
    if 'uid' in request.session:
        uid = request.session['uid']
    else:
        uid = None
    args['likes'] = article_model.filter(
        like=True).all().count() or None
    args['dislikes'] = article_model.filter(
        like=False).all().count() or None
    args['articles'] = Article.objects.filter(
        is_active=True).order_by('views')[:4]
    args['current_user_like'] = article_model.filter(
        article=current_article.id, user=uid).first() or None
    args['article'] = current_article

    return render(request, 'blog/article.html', args)


def tag_sort(request, tag):
    args = dict()
    args['articles'] = ArticleTag.objects.get(tag=tag).article_set.all()
    return render(request, 'blog/tags.html', args)


def create_article(request):
    args = dict()
    if 'uid' not in request.session:
        messages.error(request, _("Only registered users can write stories"))
        return redirect(reverse('users:login'))
    user = User.objects.get(id=request.session['uid'])
    form = ArticleForm(None)
    pattern = r'([a-zA-Z0-9]+)'
    comp = compile(pattern=pattern)
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
                slug = ''
                title = findall(comp, form.cleaned_data['title'].lower())
                for word in title:
                    slug += '{}_'.format(word)
                slug = slug.rstrip('_')
                new_article = Article.objects.create(
                    language=Languages.objects.get(
                        code=form.cleaned_data['language']),
                    image=ArticleImage.objects.get(
                        image=request.session['image']),
                    title=form.cleaned_data['title'],
                    description=form.cleaned_data['description'],
                    text=form.cleaned_data['text'],
                    author=user,
                    slug=slug,
                    is_active=False
                )
                new_article.save()
                request.session['article_id'] = int(new_article.id)
                args['temp_article'] = Article.objects.get(
                    id=request.session['article_id']) or None
            return render(request, 'blog/create.html', args)
        elif 'finish' in request.POST:
            tags = request.POST['tags']
            current_article = Article.objects.get(
                id=request.session['article_id'])
            if len(tags) > 1:
                args['tags'] = tags
                tags_list = list()
                tags_tmp = findall(comp, tags.lower())
                for word in tags_tmp:
                    tags_list.append(ArticleTag.objects.get_or_create(
                        tag=word, language=Languages.objects.get(
                            code=current_article.language.code))[0])
                current_article.tags.add(*tags_list)
                current_article.save()
                del request.session['article_id']
                del request.session['image']
                messages.info(request, "Your article was sent for review. You "
                                       "can edit article in your profile.")
                return redirect(reverse('users:profile',
                                        kwargs={
                                            'uid': request.session['uid']}))

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
    pattern = r'([a-zA-Z0-9]+)'
    comp = compile(pattern=pattern)

    def get(self, request, slug):
        """ Response on get query

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

        print(request.POST)

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
            print(img_form.errors)
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

        if 'save' in request.POST:
            # handler for edit article

            form = EditArticleForm(request.POST, instance=current_article)
            self.args['form'] = form
            if form.is_valid():
                current_article = form.save(commit=False)
                current_article.is_active = False
                current_article.save()
                return redirect(reverse('blog:edit_article',
                                        kwargs={'slug': slug}))
        if 'tags' in request.POST:
            # handler for add tag POST query
            tags = request.POST['tags']

            if len(tags) > 1:
                tags_tmp = findall(self.comp, tags.lower())
                for word in tags_tmp:
                    self.tags_list.append(ArticleTag.objects.get_or_create(
                        tag=word, language=Languages.objects.get(
                            code=current_article.language.code))[0])

                current_article.tags.add(*self.tags_list)
                current_article.save()
            else:
                messages.error(request,
                               _("You have to add minimum one tag"))

        if 'remove_tag' in request.POST:
            # handler for remove tag (AJAX POST query)

            if request.POST['remove_tag'].isdigit():
                tag_id = int(request.POST['remove_tag'])
            else:
                messages.error(request, _("Tag not found"))
                return redirect(reverse('blog:edit_article',
                                        kwargs={'slug': slug}))
            articl_id = int(current_article.id)

            with connection.cursor() as c:
                c.execute(
                    "SELECT id FROM public.blog_article_tags "
                    "WHERE article_id=%(aid)s AND articletag_id=%(tid)s",
                    {'aid': articl_id, 'tid': tag_id})
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
                        [articl_id])
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
