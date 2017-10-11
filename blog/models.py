from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from main.functions import get_image_path
from main.models import Languages
from users.models import User


class ArticleImage(models.Model):
    name = models.CharField(_("name"), max_length=64, blank=True, null=True, default=None)
    image = models.ImageField(_("image"), upload_to=get_image_path,
                              default='/static/img/no_image.png')
    user = models.ForeignKey(User)
    is_active = models.BooleanField(_("is active"), default=True)
    created = models.DateTimeField(verbose_name=_("created"),
                                   auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(verbose_name=_("updated"),
                                   auto_now_add=False, auto_now=True)

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = _('Photo')
        verbose_name_plural = _('Photos')


class ArticleTag(models.Model):
    tag = models.CharField(_("tag"), max_length=65, default=None)
    language = models.ForeignKey(Languages, verbose_name=_("language"),
                                 default=None)
    is_active = models.BooleanField(_("is active"), default=True)

    def __str__(self):
        return self.tag

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')


class Article(models.Model):
    language = models.ForeignKey(Languages, verbose_name=_("language"),
                                 default=None)
    tags = models.ManyToManyField(ArticleTag, verbose_name=_("tags"),
                                  default=None)
    image = models.ForeignKey(ArticleImage, verbose_name=_("image"),
                              default=None)
    title = models.CharField(_("title"), max_length=255, default=None,
                             unique=True)
    description = models.TextField(_("description"), default=None)
    text = models.TextField(_("text"), default=None)
    author = models.ForeignKey(User, verbose_name=_("user"), default=None)
    slug = models.CharField(_("slug"), max_length=255, default=None,
                            unique=True)
    is_active = models.BooleanField(_("is active"), default=True)
    views = models.IntegerField(default=0)

    created = models.DateTimeField(verbose_name=_("created"),
                                   auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(verbose_name=_("updated"),
                                   auto_now_add=False, auto_now=True)

    def __str__(self):

        return self.title

    class Meta:
        verbose_name = _('Article')
        verbose_name_plural = _('Articles')


class ArticleLikes(models.Model):
    user = models.ForeignKey(User, verbose_name=_("user"), )
    article = models.ForeignKey(Article, verbose_name=_("article"), )
    like = models.BooleanField(verbose_name=_("like"))

    class Meta:
        db_table = 'blog_article_likes'


class ArticleViewsPerDay(models.Model):
    article = models.ForeignKey(Article, verbose_name=_("article"))
    date = models.DateField(_('date'), default=timezone.now)
    views = models.IntegerField(_('views'), default=0)

    def __str__(self):
        return self.article.title

    class Meta:
        db_table = "article_views_per_day"
