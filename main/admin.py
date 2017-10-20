from __future__ import unicode_literals
from django.contrib import admin
from .models import Pages, Message, Languages

register = admin.site.register


class UsersActionsLanguageAdmin(admin.ModelAdmin):
    list_display = ['code', 'is_active']

    class Meta:
        model = Languages


register(Languages, UsersActionsLanguageAdmin)


class PageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Pages._meta.fields]

    class Meta:
        model = Pages


register(Pages, PageAdmin)


class PagesAdmin(admin.ModelAdmin):
    list_display = ["title",
                    "email",
                    "username",
                    "date"]

    class Meta:
        model = Message


register(Message, PagesAdmin)
