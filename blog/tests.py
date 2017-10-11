# encoding: utf-8
from django.test import TestCase
from django.urls import reverse

from main.models import Languages as Lang
from users.models import User
from .models import ArticleImage, Article, ArticleTag as Tag

from .views import *


class BlogTests(TestCase):
    def setUp(self):
        self.lang = Lang.objects.create(code='en', is_active=True)
        self.lang = Lang.objects.create(code='ru', is_active=True)
        self.user = User.objects.create_user(email='user@example.com',
                                             first_name='John',
                                             last_name='Doe',
                                             password='Super_password')
        self.tag = Tag.objects.create(tag="test", is_active=True,
                                      language=Lang.objects.get(code='en'))
        self.image = ArticleImage.objects.create(name='Test',
                                                 image='path/to/image/',
                                                 is_main=True,
                                                 is_active=True)
        self.article = Article.objects.create(
            image=ArticleImage.objects.get(name='Test'),
            language=Lang.objects.get(code='en'),
            title='Article title',
            description='Short description',
            slug='test_article',
            text='Short text',
            author=User.objects.get(pk=self.user.pk))

    def test_blog_articles(self):
        response = self.client.get(reverse('blog:articles'))
        self.assertEqual(response.status_code, 200)

    def test_blog_article(self):
        response = self.client.get(
            reverse('blog:article', kwargs={'slug': self.article.slug}))
        self.assertEqual(response.status_code, 200)

    def test_blog_tag_sort(self):
        a = self.article
        a.tags.add(self.tag)
        response = self.client.get(
            reverse('blog:tag', kwargs={'tag': self.tag}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.find(self.article.title.encode('utf-8')) > -1)
