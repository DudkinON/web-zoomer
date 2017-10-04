from django.db import models
from django.utils.translation import ugettext_lazy as _
from PIL import Image
from main.functions import get_image_path


class Pages(models.Model):
    title = models.CharField(_("title"), max_length=128, blank=True, null=True, default=None)
    text = models.TextField(_("text"), blank=True, null=True, default=None)
    image = models.ImageField(_("image"), upload_to=get_image_path, max_length=255, blank=True, null=True, default=None)

    def __str__(self):
        return _("Title: {}").format(self.title)

    class Meta:
        verbose_name = _('Page')
        verbose_name_plural = _('Pages')


class Message(models.Model):
    username = models.CharField(_("username"), max_length=64)
    title = models.CharField(_("title"), max_length=100, blank=True, null=True, default=None)
    email = models.EmailField(_("email"), max_length=40)
    text = models.CharField(_("text"), max_length=250, default=None)
    data = models.DateTimeField(_("data"), auto_now_add=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self):
        return "{}".format(self.username)

    class Meta:
        db_table = 'main_message'
        verbose_name = _('Message')
        verbose_name_plural = _('Messages')
