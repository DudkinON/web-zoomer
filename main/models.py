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


class Message(models.Model):
    username = models.CharField(max_length=64)
    title = models.CharField(max_length=100, blank=True, null=True, default=None)
    email = models.EmailField(max_length=40)
    text = models.CharField(max_length=250, default=None)
    data = models.DateTimeField(auto_now_add=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "{}".format(self.username)

    class Meta:
        db_table = 'main_message'
        verbose_name = 'Message'
        verbose_name_plural = 'Messages'
