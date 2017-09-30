from django.conf.urls import url
from .views import UsersLoginFormView, logout_view, RegisterUserView, user_activation

app_name = 'users'

urlpatterns = [
    url(r'^login/', UsersLoginFormView.as_view(), name='login'),
    url(r'^register/', RegisterUserView.as_view(), name='register'),
    url(r'^logout/', logout_view, name='logout'),
    url(r'^users/activate/(?P<uid>\w+)/(?P<code>\w+)', user_activation,
        name='activate'),
]
