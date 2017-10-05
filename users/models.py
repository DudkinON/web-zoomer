from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(_('password'), max_length=128)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('is active'), default=False)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the user can log into this admin site')
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'auth_user'
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_full_name(self):
        """Returns the first_name plus the last_name, with a space in between.

        :return string:
        """
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Returns the short name for the user.

        :return string:
        """
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Sends an email to this User.

        :param subject:
        :param message:
        :param from_email:
        :param kwargs:
        :return void:
        """
        from django.core.mail import send_mail
        send_mail(subject, message, from_email, [self.email], **kwargs)


class ActionSlug(models.Model):
    slug = models.CharField(_('slug'), max_length=60, primary_key=True)

    def __str__(self):
        return "{}".format(self.slug)

    class Meta:
        verbose_name = _('Slug')
        verbose_name_plural = _('Slugs')


class ActionLanguage(models.Model):
    name = models.CharField(max_length=4, primary_key=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        lang = _("Language")
        return "{}: {}".format(lang, self.name)

    class Meta:
        verbose_name = _('Language')
        verbose_name_plural = _('Languages')


class Action(models.Model):
    name = models.CharField(_('name'), max_length=60, default=None, unique=True)
    slug = models.ForeignKey(ActionSlug, max_length=60, default=None)
    language = models.ForeignKey(ActionLanguage, default=None)
    is_active = models.BooleanField(_('is active'), default=False)

    def __str__(self):
        action = _("Action")
        return "{}: {}".format(action, self.name)

    class Meta:
        verbose_name = _('Action')
        verbose_name_plural = _('Actions')
