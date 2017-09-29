from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.articles, name='articles'),
    url(r'^(?P<article_id>\w+)$', views.article, name='article'),
    url(r'^category/(?P<category_id>\w+)$', views.category, name='category')
]
