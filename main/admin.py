from django.contrib import admin
from .models import Pages, Message, Category


class PageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Pages._meta.fields]

    class Meta:
        model = Pages


admin.site.register(Pages, PageAdmin)


class CategoriesPagesAdmin(admin.ModelAdmin):
    list_display = ["title"]

    class Meta:
        model = Category


admin.site.register(Category, CategoriesPagesAdmin)


class PagesAdmin(admin.ModelAdmin):
    list_display = ["title",
                    "email",
                    "category",
                    "username",
                    "data"]

    class Meta:
        model = Message


admin.site.register(Message, PagesAdmin)
