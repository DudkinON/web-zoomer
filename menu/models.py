from django.db import models


class Menu(models.Model):
    name = models.CharField(max_length=128)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return "Menu item: %s" % self.name

    class Meta:
        verbose_name = 'Menu item'
        verbose_name_plural = 'Menu items'
