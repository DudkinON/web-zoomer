# encoding: utf-8
from django.test import TestCase, RequestFactory
from users.models import User
from blog.models import ArticleImage, Article, ArticleTag as Tag
from django.urls import reverse
from main.models import Languages as Lang
from .views import *


class MainTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.lang = Lang.objects.create(code='en', is_active=True)
        self.lang = Lang.objects.create(code='ru', is_active=True)
        self.user = User.objects.create_user(email='user@example.com',
                                             first_name='John',
                                             last_name='Doe',
                                             password='Super_password')
        self.category = Tag.objects.create(tag="test", is_active=True,
                                           language=Lang.objects.get(code='en'))
        self.image = ArticleImage.objects.create(name='Test',
                                                 image='path/to/image/',
                                                 is_main=True,
                                                 is_active=True)
        self.article = Article.objects.create(
            tags=Tag.objects.get(tag="test"),
            image=ArticleImage.objects.get(name='Test'),
            title='Article title',
            key_words='key, word',
            description='Short description',
            slug='test-article',
            text='Short text',
            author=User.objects.get(email='user@example.com'))

    def test_main_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_main_about(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)

    def test_main_contacts(self):
        data = {"email": "user@example.com",
                "username": "John",
                "title": "Test",
                "text": "Test text message"}

        response_get = self.client.get(reverse('contacts'))
        response_post = self.client.post(path=reverse('contacts'), data=data)
        message = Message.objects.get(email="user@example.com") or None
        self.assertEqual(message.email, data['email'])
        self.assertEqual(message.title, data['title'])
        self.assertEqual(message.username, data['username'])
        self.assertEqual(message.text, data['text'])
        self.assertEqual(response_get.status_code, 200)
        self.assertEqual(response_post.status_code, 302)

    def test_main_language_ru(self):
        response = self.client.get(reverse('language', kwargs={'lang': 'ru'}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session[LANGUAGE_SESSION_KEY], 'ru')

    def test_main_language_en(self):
        response = self.client.get(reverse('language', kwargs={'lang': 'en'}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.client.session[LANGUAGE_SESSION_KEY], 'en')

    def test_main_search(self):
        response = self.client.get('/search/?q=Article+title')
        tmp = str(response.content)
        self.assertTrue(tmp.find('Article title') > -1)
