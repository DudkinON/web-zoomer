from django.shortcuts import render

from blog.models import Article, ArticleLikes


app_name = 'blog'


def articles(request):
    args = dict()
    args['articles'] = Article.objects.filter(
        is_active=True).order_by("-created")[:3]
    args['title'] = 'Articles'
    args['page'] = 'Blog page'
    return render(request, 'blog/index.html', args)


def article(request, article_id):
    args = dict()
    article_model = ArticleLikes.objects
    current_article = Article.objects.get(id=article_id)
    current_article.views += 1
    current_article.save(update_fields='views')
    if 'uid' in request.session:
        uid = request.session['uid']
    else:
        uid = None
    args['likes'] = article_model.filter(
        like=True).all().count() or None
    args['dislikes'] = article_model.filter(
        like=False).all().count() or None
    args['articles'] = Article.objects.filter(
        is_active=True).order_by("-date")[:4]
    args['current_user_like'] = article_model.filter(
        article=article_id, user=uid).first() or None
    args['article'] = current_article

    return render(request, 'blog/article.html', args)


def tag_sort(request, tag):
    args = dict()
    args['articles'] = Article.objects.filter(is_active=True,
                                           tags=tag).order_by("-created")[:4]
    return render(request, 'blog/category.html', args)
