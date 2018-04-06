from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from imagekit.models import ProcessedImageField
from pilkit.processors import ResizeToFill

from main.functions import get_image_path
from main.models import Languages
from users.models import User, Readers


class ArticleImage(models.Model):
    image = ProcessedImageField(verbose_name=_("image"),
                                upload_to=get_image_path,
                                processors=[ResizeToFill(1000, 800)],
                                format='JPEG',
                                options={'quality': 80})
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(_("is active"), default=True)
    created = models.DateTimeField(verbose_name=_("created"),
                                   auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(verbose_name=_("updated"),
                                   auto_now_add=False, auto_now=True)

    def __str__(self):
        return "user: {}, image id: {}".format(
            self.user.get_full_name, self.id)

    class Meta:
        db_table = "article_image"
        verbose_name = _('Image')
        verbose_name_plural = _('Images')


class ArticleTag(models.Model):
    tag = models.CharField(_("tag"), max_length=65, default=None)
    language = models.ForeignKey(Languages, verbose_name=_("language"),
                                 default=None, on_delete=models.DO_NOTHING)
    is_active = models.BooleanField(_("is active"), default=True)

    def __str__(self):
        return self.tag

    class Meta:
        db_table = "article_tag"
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')

    @property
    def serialize(self):
        return {
            'tag': self.tag,
            'language': self.language.serialize,
            'is_active': self.is_active
        }


class Article(models.Model):
    language = models.ForeignKey(Languages, verbose_name=_("language"),
                                 default=None, on_delete=models.DO_NOTHING)
    tags = models.ManyToManyField(ArticleTag, verbose_name=_("tags"),
                                  default=None)
    image = models.ForeignKey(ArticleImage, verbose_name=_("image"),
                              default=None, on_delete=models.DO_NOTHING)
    title = models.CharField(_("title"), max_length=255, default=None,
                             unique=True)
    description = models.TextField(_("description"), default=None)
    text = models.TextField(_("text"), default=None)
    author = models.ForeignKey(User, verbose_name=_("user"), default=None,
                               on_delete=models.DO_NOTHING)
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

    @property
    def serialise(self):
        return {
            'language': self.language.serialize,
            'tags': self.tags,
            'image': self.image,
            'title': self.title,
            'description': self.description,
            'text': self.text,
            'author': self.author,
            'slug': self.slug,
            'is_active': self.is_active,
            'views': self.views,
            'created': self.created,
            'updated': self.updated
        }

    @property
    def count_published_articles_by_author(self):
        """Return amount of published articles

        :return int:
        """
        return Article.objects.filter(
            author_id=self.author_id).all().count() or 0

    @property
    def count_readers(self):
        """Return amount of readers by author

        :return int:
        """
        return Readers.objects.filter(
            author_id=self.author_id).all().count() or 0


class ArticleLikes(models.Model):
    user = models.ForeignKey(User,
                             verbose_name=_("user"),
                             on_delete=models.DO_NOTHING)
    article = models.ForeignKey(Article,
                                verbose_name=_("article"),
                                on_delete=models.DO_NOTHING)
    like = models.BooleanField(verbose_name=_("like"))

    class Meta:
        db_table = 'blog_article_likes'


class ArticleViewsPerDay(models.Model):
    article = models.ForeignKey(Article,
                                verbose_name=_("article"),
                                on_delete=models.DO_NOTHING)
    date = models.DateField(_('date'), default=timezone.now)
    views = models.IntegerField(_('views'), default=0)

    def __str__(self):
        return self.article.title

    class Meta:
        db_table = "article_views_per_day"


class Bookmarks(models.Model):
    reader = models.ForeignKey(User,
                               related_name=_("user"),
                               on_delete=models.DO_NOTHING)
    article = models.ForeignKey(Article,
                                related_name=_("article"),
                                on_delete=models.DO_NOTHING)
