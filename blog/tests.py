from __future__ import unicode_literals

from importlib import import_module
from django.test import TestCase
from django.conf import settings

from main.models import Languages as Lang
from .models import ArticleTag as Tag

from .views import *


class BlogTests(TestCase):
    def setUp(self):
        settings.SESSION_ENGINE = 'django.contrib.sessions.backends.file'
        engine = import_module(settings.SESSION_ENGINE)
        store = engine.SessionStore()
        store.save()
        self.session = store
        self.client.cookies[settings.SESSION_COOKIE_NAME] = store.session_key
        self.lang = Lang.objects.create(code='en', is_active=True)
        self.lang = Lang.objects.create(code='ru', is_active=True)
        self.user = User.objects.create_user(email='user@example.com',
                                             first_name='John',
                                             last_name='Doe',
                                             password='Super_password')
        self.tag = Tag.objects.create(tag="test", is_active=True,
                                      language=Lang.objects.get(code='en'))
        self.image = ArticleImage.objects.create(user=self.user,
                                                 image='path/to/image/',
                                                 is_active=True)
        self.article = Article.objects.create(
            image=ArticleImage.objects.get(id=self.image.id),
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

        # check post like with not logged user
        response = self.client.post(reverse(
            'blog:article', kwargs={'slug': self.article.slug}),
            {'like': 1})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:login'))

        # check post like with logged user
        new_user = User.objects.create(email='example@example.com',
                                       first_name='newJohn',
                                       last_name='newDoe',
                                       password='newSuper_password')
        self.session['uid'] = int(new_user.id)
        self.session.save()
        response = self.client.post(reverse(
            'blog:article', kwargs={'slug': self.article.slug}),
            {'like': 1})
        self.assertEqual(response.status_code, 200)

        # check quantity of likes/dislikes after post query
        likes = ArticleLikes.objects.filter(like=True).all().count()
        dislikes = ArticleLikes.objects.filter(like=False).all().count()
        self.assertEqual(int(likes), 1)
        self.assertEqual(int(dislikes), 0)

        # login new user and send post query
        self.session['uid'] = int(self.user.id)
        self.session.save()
        response = self.client.post(reverse(
            'blog:article', kwargs={'slug': self.article.slug}),
            {'like': 1})
        self.assertEqual(response.status_code, 200)

        # check amount of likes/dislikes after add one more vote
        likes = ArticleLikes.objects.filter(like=True).all().count()
        dislikes = ArticleLikes.objects.filter(like=False).all().count()
        self.assertEqual(int(likes), 2)
        self.assertEqual(int(dislikes), 0)

        # change vote on dislike
        response = self.client.post(reverse(
            'blog:article', kwargs={'slug': self.article.slug}),
            {'like': 0})
        self.assertEqual(response.status_code, 200)

        # check amount of likes/dislikes after changes
        likes = ArticleLikes.objects.filter(like=True).all().count()
        dislikes = ArticleLikes.objects.filter(like=False).all().count()
        self.assertEqual(int(likes), 1)
        self.assertEqual(int(dislikes), 1)

    def test_blog_tag_sort(self):
        a = self.article
        a.tags.add(self.tag)
        response = self.client.get(
            reverse('blog:tag', kwargs={'tag': self.tag}))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.content.find(
            self.article.title.encode('utf-8')) > -1)

    def test_blog_create_article(self):
        # check access to page not logged user
        response = self.client.get(reverse('blog:create_article'))
        self.assertEqual(response.status_code, 302)

        # check access to page logged user
        self.assertEqual(response.url, reverse('users:login'))
        self.session['uid'] = self.user.id
        self.session.save()
        response = self.client.get(reverse('blog:create_article'))
        self.assertEqual(response.status_code, 200)

        # create image and add to session
        image = ArticleImage.objects.create(user=self.user,
                                            image='path/to/new/image/',
                                            is_active=True)
        self.session['image'] = str(image.image)
        self.session.save()

        # check create article post query
        response = self.client.post(
            reverse('blog:create_article'),
            {'title': 'New title',
             'description': 'New description',
             'text': 'new text',
             'language': 'en',
             'create': ''}
        )
        self.assertEqual(response.status_code, 200)

        # check add tags post query
        response = self.client.post(
            reverse('blog:create_article'),
            {'tags': 'New title',
             'finish': ''}
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse(
            'users:profile', kwargs={'uid': self.session['uid']}))
        curr_art = Article.objects.get(title='New title') or None
        self.assertEqual(curr_art.title, 'New title')
        self.assertEqual(curr_art.description, 'New description')
        self.assertEqual(curr_art.text, 'new text')
        self.assertEqual(curr_art.language.code, 'en')
        self.assertEqual(curr_art.tags.first().tag, 'new')

    def test_blog_edit_article(self):
        # check access to page not logged user
        response = self.client.get(reverse('blog:edit_article',
                                           kwargs={'slug': self.article.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:login'))

        # check access to page wrong author
        new_user = User.objects.create(email='example@example.com',
                                       first_name='newJohn',
                                       last_name='newDoe',
                                       password='newSuper_password')
        self.session['uid'] = new_user.id
        self.session.save()
        response = self.client.get(reverse('blog:edit_article',
                                           kwargs={'slug': self.article.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:profile',
                                               kwargs={'uid': new_user.id}))

        # check the article author access to page
        self.session['uid'] = self.user.id
        self.session.save()
        response = self.client.get(reverse('blog:edit_article',
                                           kwargs={'slug': self.article.slug}))
        self.assertEqual(response.status_code, 200)

        # check post query
        image = ArticleImage.objects.create(user=self.user,
                                            image='path/to/old/image/',
                                            is_active=True)
        new_article = Article.objects.create(
            image=ArticleImage.objects.get(id=image.id),
            language=Lang.objects.get(code='en'),
            title='Old article title',
            description='old description',
            slug='old_article_title',
            text='old article text',
            author=User.objects.get(pk=self.user.pk))
        aid = int(new_article.id)
        response = self.client.post(
            reverse('blog:edit_article', kwargs={'slug': new_article.slug}),
            {'save': '',
             'title': 'Новое название',
             'description': 'New description',
             'text': 'новый текст',
             'language': 'ru',
             })
        self.assertEqual(response.status_code, 302)
        new_article = Article.objects.get(id=aid)
        self.assertEqual(new_article.id, aid)
        self.assertEqual(new_article.title, 'Новое название')
        self.assertEqual(new_article.description, 'New description')
        self.assertEqual(new_article.text, 'новый текст')
        self.assertEqual(new_article.language.code, 'ru')
        self.assertEqual(new_article.slug, 'новое_название')

    def test_blog_author_articles(self):
        response = self.client.get(reverse(
            'blog:author_articles', kwargs={'uid': self.user.id}))
        self.assertEqual(response.status_code, 200)

    def test_blog_delete_article(self):

        # check access to page not logged user
        response = self.client.get(reverse(
            'blog:delete_article', kwargs={'slug': self.article.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('users:login'))

        # check access to page wrong author
        new_user = User.objects.create(email='example@example.com',
                                       first_name='newJohn',
                                       last_name='newDoe',
                                       password='newSuper_password')
        self.session['uid'] = int(new_user.id)
        self.session.save()
        response = self.client.get(reverse(
            'blog:delete_article', kwargs={'slug': self.article.slug}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse(
            'users:profile', kwargs={'uid': self.session['uid']}))

        # check access to page author the article
        article_id = int(self.article.id)
        self.session['uid'] = self.user.id
        self.session.save()
        response = self.client.get(reverse(
            'blog:delete_article', kwargs={'slug': self.article.slug}))
        self.assertEqual(response.status_code, 200)
        response = self.client.post(reverse(
            'blog:delete_article', kwargs={'slug': self.article.slug}),
            {'title': self.article.title})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse(
            'users:profile', kwargs={'uid': self.user.id}))
        deleted_article = Article.objects.filter(id=article_id) or None
        self.assertEqual(deleted_article, None)
