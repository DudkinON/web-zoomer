from django.contrib import admin

from blog.models import Article, ArticleTag, ArticleImage


register = admin.site.register


class ArticleAdmin(admin.ModelAdmin):
    list_display = ["title",
                    "author",
                    "is_active",
                    "views"]

    class Meta:
        model = Article


register(Article, ArticleAdmin)


class ArticleTagAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ArticleTag._meta.fields]

    class Meta:
        model = ArticleTag


register(ArticleTag, ArticleTagAdmin)


class ArticleImageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ArticleImage._meta.fields]

    class Meta:
        model = ArticleImage


register(ArticleImage, ArticleImageAdmin)
