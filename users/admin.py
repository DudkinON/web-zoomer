from django.contrib import admin
from .models import User, Action, ActionLanguage

register = admin.site.register


class UsersAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active')
    search_fields = ['email']

    class Meta:
        model = User


register(User, UsersAdmin)


class UsersActionsLanguageAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']

    class Meta:
        model = ActionLanguage


register(ActionLanguage, UsersActionsLanguageAdmin)


class UsersActionsAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active']

    class Meta:
        model = Action


register(Action, UsersActionsAdmin)
