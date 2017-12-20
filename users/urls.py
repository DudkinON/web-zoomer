from __future__ import unicode_literals

from django.conf.urls import url
from .views import UsersLoginFormView, logout_view, RegisterUserView
from .views import user_activation, UserProfile, OAuthUserView

app_name = 'users'

urlpatterns = [
    url(r'^login/', UsersLoginFormView.as_view(), name='login'),
    url(r'^register/', RegisterUserView.as_view(), name='register'),
    url(r'^oauth/(?P<provider>\w+)', OAuthUserView.as_view(), name='oauth'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^profile/(?P<uid>\w+)/', UserProfile.as_view(), name='profile'),
    url(r'^activate/(?P<uid>\w+)/(?P<code>\w+)/', user_activation,
        name='activate'),
]
