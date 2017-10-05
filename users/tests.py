# encoding: utf-8
from __future__ import unicode_literals
from django.test import TestCase, RequestFactory
from django.core import mail
from django.urls import reverse, reverse_lazy
from django.utils.six import text_type
from django.utils.translation import LANGUAGE_SESSION_KEY

from .views import *
from .models import ActionLanguage as Lang, ActionSlug as Slug, Action


class UsersTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            email='user@example.com', first_name='John', last_name='Doe',
            password='Super_password')
        self.lang = Lang.objects.create(name='en', is_active=True)
        self.lang = Lang.objects.create(name='ru', is_active=True)
        self.slug = Slug.objects.create(slug='test')
        self.action = Action.objects.create(slug=Slug.objects.get(slug='test'),
                                            language=Lang.objects.get(name='en'),
                                            name='test')
        self.action = Action.objects.create(slug=Slug.objects.get(slug='test'),
                                            language=Lang.objects.get(name='ru'),
                                            name='тест')

    def test_users_login(self):
        response_get = self.client.get(path='/users/login/')
        response_post = self.client.post('/users/login/',
                                         {"email": "user@example.com",
                                          "password": "Super_password"})
        self.assertEqual(response_get.status_code, 200)
        self.assertEqual(response_post.status_code, 302)

    def test_users_register(self):
        response_get = self.client.get('/users/register/')
        response_post = self.client.post('/users/register/',
                                         {"email": "email@email.com",
                                          "first_name": "John",
                                          "last_name": "Doe",
                                          "password": "password",
                                          "confirm_password": "password", })
        user = User.objects.filter(email="email@email.com").first() or None
        user_code = hashed((user.email + user.password).encode('utf-8')
                           ).hexdigest()
        url = "{}/users/activate/{}/{}/".format(SITE_URL, user.id, user_code)

        self.assertTrue(
            text_type(mail.outbox[0].message()).find("text/plain") > -1)
        self.assertTrue(text_type(mail.outbox[0].message()).find(url) > -1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].to, [user.email])
        self.assertFalse(user.is_active)
        self.assertEqual(user.email, "email@email.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")
        self.assertEqual(response_get.status_code, 200)
        self.assertEqual(response_post.status_code, 302)

    def test_users_logout(self):
        response = self.client.get('/users/logout/')
        self.assertEqual(response.status_code, 302)

    def test_users_activate(self):
        user = User.objects.filter(email="user@example.com").first() or None
        user_code = hashed((user.email + user.password).encode('utf-8')
                           ).hexdigest()
        url = '/users/activate/{}/{}/'.format(user.id, user_code)
        response = self.client.get(url)
        user = User.objects.filter(email="user@example.com").first() or None
        self.assertTrue(user.is_active)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/users/profile/')

    def test_users_profile(self):
        response = self.client.get(reverse('users:profile', kwargs={'uid': 1}))
        self.assertTrue(response.status_code, 200)

    def test_users_action_en(self):
        slug = Action.objects.filter(slug='test').first().slug
        self.client.get(reverse('language', kwargs={'lang': 'en'}))
        response = self.client.get('/users/profile/action/{}/'.format(slug))
        tmp = str(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(tmp.find('test') > -1)
        self.assertTrue(tmp.find('en') > -1)

    def test_users_action_ru(self):
        slug = Action.objects.filter(slug='test').first().slug
        self.client.get(reverse('language', kwargs={'lang': 'ru'}))
        response = self.client.get('/users/profile/action/{}/'.format(slug))
        tmp = str(response.content.decode('utf-8'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(tmp.find('тест') > -1)
        self.assertTrue(tmp.find('ru') > -1)
