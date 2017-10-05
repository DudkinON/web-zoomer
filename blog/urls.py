from django.conf.urls import url

from . import views

app_name = 'blog'

urlpatterns = [
    url(r'^$', views.articles, name='articles'),
    url(r'^tag/(?P<tag>\w+)/$', views.tag_sort, name='tag'),
    url(r'^create/$', views.article, name='article_create'),
    url(r'^update/(?P<article_id>\w+)/$', views.article,
        name='article_update'),
    url(r'^delete/(?P<article_id>\w+)/$', views.article, name='article'),
    url(r'^(?P<article_id>\w+)/$', views.article, name='article')
]
