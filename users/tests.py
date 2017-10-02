# encoding: utf-8
from __future__ import unicode_literals
from django.test import TestCase, RequestFactory
from django.core import mail
from django.utils.six import text_type
from django.urls import reverse
from .views import *
from .models import *


class UsersTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            email='user@example.com', first_name='John', last_name='Doe',
            password='Super_password')

    def test_user_login(self):
        response_get = self.client.get(path='/users/login/')
        response_post = self.client.post('/users/login/',
                                         {"email": "user@example.com",
                                          "password": "Super_password"})
        self.assertEqual(response_get.status_code, 200)
        self.assertEqual(response_post.status_code, 302)

    def test_user_register(self):
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

    def test_user_logout(self):
        response = self.client.get('/users/logout/')
        self.assertEqual(response.status_code, 302)

    def test_user_activate(self):
        user = User.objects.filter(email="user@example.com").first() or None
        user_code = hashed((user.email + user.password).encode('utf-8')
                           ).hexdigest()
        url = '/users/activate/{}/{}/'.format(user.id, user_code)
        response = self.client.get(url)
        user = User.objects.filter(email="user@example.com").first() or None
        self.assertTrue(user.is_active)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/users/profile/')
