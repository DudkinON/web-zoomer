from django.conf.urls import url
from .views import UsersLoginFormView, logout_view, RegisterUserView

app_name = 'users'

urlpatterns = [
    url(r'^login/', UsersLoginFormView.as_view(), name='login'),
    url(r'^register/', RegisterUserView.as_view(), name='register'),
    url(r'^logout/', logout_view, name='logout'),
    # url(r'^register/', 'users.views.register', name='register'),
]
