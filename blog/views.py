from django.shortcuts import render

from blog.models import Blog, Category


app_name = 'blog'


def articles(request):
    context = dict()
    context['categories'] = Category.objects.filter(is_active=True)
    context['articles'] = Blog.objects.filter(is_active=True).order_by("-date")[:3]
    context['title'] = 'Articles'
    context['page'] = 'Blog page'
    return render(request, 'blog/index.html', context)


def article(request, article_id):
    context = dict()
    context['articles'] = Blog.objects.filter(is_active=True).order_by("-date")[:4]
    context['categories'] = Category.objects.filter(is_active=True)
    context['article'] = Blog.objects.get(id=article_id)

    return render(request, 'blog/article.html', context)


def category(request, category_id):
    context = dict()
    context['articles'] = Blog.objects.filter(is_active=True, category=category_id).order_by("-date")[:4]
    context['category'] = Category.objects.get(id=category_id)
    context['categories'] = Category.objects.filter(is_active=True)
    return render(request, 'blog/category.html', context)
