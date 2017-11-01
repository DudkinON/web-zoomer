from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _

from imagekit.models import ProcessedImageField

from .managers import UserManager
from main.functions import get_user_image_path


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    password = models.CharField(_('password'), max_length=128)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    website = models.CharField(_('website'), max_length=100, null=True,
                               blank=True, default=None)
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_active = models.BooleanField(_('is active'), default=False)
    avatar = ProcessedImageField(upload_to=get_user_image_path, null=True,
                                 blank=True,
                                 default='no-photo.gif')
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

    @property
    def get_full_name(self):
        """Returns the first_name plus the last_name, with a space in between.

        :return string:
        """
        full_name = '{} {}'.format(self.first_name, self.last_name)
        return full_name.strip()

    @property
    def get_first_name(self):
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


class Readers(models.Model):
    author = models.ForeignKey(User, related_name=_("author"))
    reader = models.ForeignKey(User, related_name=_("reader"))

    @property
    def count_readers(self):
        """Return quantity of readers by author

        :return int:
        """
        return Readers.objects.filter(author=self.author).all().count() or 0



