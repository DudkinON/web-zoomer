from django.db import models
from django.utils.translation import ugettext_lazy as _
from main.functions import get_image_path
from main.models import Languages
from users.models import User


class ArticleImage(models.Model):
    name = models.CharField(_("name"), max_length=64)
    image = models.ImageField(_("image"), upload_to=get_image_path, default=None)
    is_main = models.BooleanField(_("is main"), default=False)
    is_active = models.BooleanField(_("is active"), default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')


class ArticleTag(models.Model):
    tag = models.CharField(_("tag"), max_length=65, default=None)
    language = models.ForeignKey(Languages, default=None)
    is_active = models.BooleanField(_("is active"), default=True)

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')


class Article(models.Model):
    tags = models.ForeignKey(ArticleTag, default=None)
    image = models.ForeignKey(ArticleImage, default=None)
    title = models.CharField(_("title"), max_length=255, default=None)
    key_words = models.CharField(_("key words"), max_length=255, blank=True,
                                 null=True, default=None)
    description = models.TextField(_("description"), default=None)
    text = models.TextField(_("text"), default=None)
    author = models.ForeignKey(User, default=None)
    slug = models.CharField(max_length=255, default=None)
    is_active = models.BooleanField(default=True)
    views = models.IntegerField(default=0)

    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        title = _("Title: {}")
        return _("{}: {}").format(title, self.title)

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')


class ArticleLikes(models.Model):
    user = models.ForeignKey(User)
    article = models.ForeignKey(Article)
    like = models.BooleanField()

    class Meta:
        db_table = 'blog_article_likes'

