from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.contrib import messages
from re import findall, compile

from blog.forms import ArticleForm, ImageForm
from blog.models import Article, ArticleLikes, ArticleTag, ArticleImage
from users.models import User
from main.models import Languages

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
    # args['articles'] = Article.objects.filter(
    #     is_active=True,
    #     tags=tag).order_by("-created")[:4]
    args['articles'] = ArticleTag.objects.get(tag=tag).article_set.all()
    return render(request, 'blog/tags.html', args)


def create_article(request):
    args = dict()
    if 'uid' not in request.session:
        messages.error(request, _("Only registered users can write stories"))
        return redirect(reverse('blog:articles'))
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
            if len(tags) > 0:
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
                return redirect(reverse('user:profile',
                                kwargs={'uid': request.session['uid']}))

            else:
                messages.error(request, _("Tag can't be empty"))
    if 'article_id' in request.session:
        args['temp_article'] = Article.objects.get(
            id=request.session['article_id']) or None
    return render(request, 'blog/create.html', args)


def edit_article(request, slug):
    args = dict()
    return render(request, 'blog/edit-article.html', args)


def delete_article(request, slug):
    args = dict()
    return render(request, 'blog/delete-article.html', args)
