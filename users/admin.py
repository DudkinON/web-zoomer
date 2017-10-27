from __future__ import unicode_literals
from django.contrib import admin
from .models import User

register = admin.site.register


class UsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active')
    search_fields = ['email']

    class Meta:
        model = User


register(User, UsersAdmin)
