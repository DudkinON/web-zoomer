from django.contrib import admin
from .models import User


class UsersAdmin(admin.ModelAdmin):

    list_display = ('email', 'first_name', 'last_name', 'is_active')
    search_fields = ['email']

admin.site.register(User, UsersAdmin)

