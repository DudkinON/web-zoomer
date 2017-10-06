from django.shortcuts import render, get_object_or_404

from blog.models import Article, ArticleLikes

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
    # current_article = Article.objects.get(slug=slug)
    article_model = ArticleLikes.objects
    print(current_article.views)
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
    args['articles'] = Article.objects.filter(
        is_active=True,
        tags=tag).order_by("-created")[:4]
    return render(request, 'blog/category.html', args)


def create_article(request):
    args = dict()
    return render(request, 'blog/category.html', args)
