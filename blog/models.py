from django.db import models

from main.functions import get_image_path


# class ArticleComments(models.Model):
#     text = models.TextField(blank=True, null=True, default=None)
#     author = models.ForeignKey


class ArticleImage(models.Model):
    name = models.CharField(max_length=64)
    image = models.ImageField(upload_to=get_image_path, max_length=255, default=None)
    is_main = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "%s" % self.name

    class Meta:
        verbose_name = 'Photo'
        verbose_name_plural = 'Photos'


class Category(models.Model):
    title = models.CharField(max_length=65, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "Category: %s" % self.title

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Blog(models.Model):
    category = models.ForeignKey(Category, blank=True, null=True, default=None)
    image = models.ForeignKey(ArticleImage, blank=True, null=True, default=None)
    title = models.CharField(max_length=255, blank=True, null=False, default=None)
    key_words = models.CharField(max_length=255, blank=True, null=True, default=None)
    description = models.TextField(blank=True, null=True, default=None)
    text = models.TextField(blank=True, null=True, default=None)
    date = models.DateTimeField(auto_now_add=True, blank=True)
    author = models.CharField(max_length=125, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return "Title: %s" % self.title

    class Meta:
        verbose_name = 'Article'
        verbose_name_plural = 'Articles'

