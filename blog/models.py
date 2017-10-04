from django.db import models
from django.utils.translation import ugettext_lazy as _
from main.functions import get_image_path


# class ArticleComments(models.Model):
#     text = models.TextField(blank=True, null=True, default=None)
#     user = models.ForeignKey


class ArticleImage(models.Model):
    name = models.CharField(_("name"), max_length=64)
    image = models.ImageField(_("image"), upload_to=get_image_path, max_length=255, default=None)
    is_main = models.BooleanField(_("is main"), default=False)
    is_active = models.BooleanField(_("is active"), default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')


class Category(models.Model):
    title = models.CharField(_("title"), max_length=65, blank=True, null=True, default=None)
    is_active = models.BooleanField(_("is active"), default=True)

    def __str__(self):
        return _("Category: {}").format(self.title)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')


class Blog(models.Model):
    category = models.ForeignKey(Category, blank=True, null=True, default=None)
    image = models.ForeignKey(ArticleImage, blank=True, null=True, default=None)
    title = models.CharField(_("title"), max_length=255, blank=True, null=False, default=None)
    key_words = models.CharField(_("key words"), max_length=255, blank=True, null=True, default=None)
    description = models.TextField(_("description"), blank=True, null=True, default=None)
    text = models.TextField(_("text"), blank=True, null=True, default=None)
    date = models.DateTimeField(_("date"), auto_now_add=True, blank=True)
    author = models.CharField(_("author"), max_length=125, blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    views = models.IntegerField(default=0)

    def __str__(self):
        return _("Title: {}").format(self.title)

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')

