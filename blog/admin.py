from django.contrib import admin

from blog.models import Blog, Category, ArticleImage


class BlogAdmin(admin.ModelAdmin):
    list_display = ["title",
                    "category",
                    "key_words",
                    "author",
                    "is_active",
                    "views"]

    class Meta:
        model = Blog

admin.site.register(Blog, BlogAdmin)


class CategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Category._meta.fields]

    class Meta:
        model = Category

admin.site.register(Category, CategoryAdmin)


class ArticleImageAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ArticleImage._meta.fields]

    class Meta:
        model = ArticleImage

admin.site.register(ArticleImage, ArticleImageAdmin)
