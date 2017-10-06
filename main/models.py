from django.db import models
from django.utils.translation import ugettext_lazy as _
from PIL import Image
from main.functions import get_image_path


class Languages(models.Model):
    code = models.CharField(max_length=4, primary_key=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        lang = _("Language")
        return "{}: {}".format(lang, self.code)

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')


class Pages(models.Model):
    title = models.CharField(_("title"), max_length=128, blank=True, null=True, default=None)
    text = models.TextField(_("text"), blank=True, null=True, default=None)
    image = models.ImageField(_("image"), upload_to=get_image_path, max_length=255, blank=True, null=True, default=None)

    def __str__(self):
        title = _("Title")
        return "{}: {}".format(title, self.title)

    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')


class Message(models.Model):
    username = models.CharField(_("username"), max_length=64)
    title = models.CharField(_("title"), max_length=100, blank=True, null=True, default=None)
    email = models.EmailField(_("email"), max_length=40)
    text = models.CharField(_("text"), max_length=250, default=None)
    date = models.DateTimeField(_("date"), auto_now=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "{}".format(self.username)

    class Meta:
        db_table = 'main_message'
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
