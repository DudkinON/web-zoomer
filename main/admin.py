from django.contrib import admin
from .models import Pages, Message


class PageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Pages._meta.fields]

    class Meta:
        model = Pages


admin.site.register(Pages, PageAdmin)


class PagesAdmin(admin.ModelAdmin):
    list_display = ["title",
                    "email",
                    "username",
                    "data"]

    class Meta:
        model = Message


admin.site.register(Message, PagesAdmin)
