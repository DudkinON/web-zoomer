from django.db import models
from PIL import Image
from main.functions import get_image_path


class Pages(models.Model):
    title = models.CharField(max_length=128, blank=True, null=True, default=None)
    text = models.TextField(blank=True, null=True, default=None)
    image = models.ImageField(upload_to=get_image_path, max_length=255, blank=True, null=True, default=None)

    def __str__(self):
        return "Title: %s" % self.title

    class Meta:
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'


class Category(models.Model):
    title = models.CharField(max_length=65, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "Category: {}".format(self.title)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


class Message(models.Model):
    username = models.CharField(max_length=64)
    title = models.CharField(max_length=100, blank=True, null=True, default=None)
    email = models.EmailField(max_length=40)
    text = models.CharField(max_length=250, default=None)
    category = models.ForeignKey(Category, blank=True, null=True, default=None)
    data = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "{}".format(self.username)

    class Meta:
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
