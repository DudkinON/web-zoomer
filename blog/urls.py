from __future__ import unicode_literals

from django.conf.urls import url

from . import views

app_name = 'blog'

urlpatterns = [
    url(r'^$', views.articles, name='articles'),
    url(r'^tag/(?P<tag>[a-zа-я]+)/$', views.tag_sort, name='tag'),
    url(r'^author/(?P<uid>\w+)/$', views.author_articles, name='author_articles'),
    url(r'^create/$', views.create_article, name='create_article'),
    url(r'^edit/(?P<slug>\w+)/$', views.EditArticle.as_view(), name='edit_article'),
    url(r'^delete/(?P<slug>\w+)/$', views.delete_article,
        name='delete_article'),
    url(r'^(?P<slug>\w+)/$', views.article, name='article')
]
