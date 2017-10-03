from django.conf.urls import url
from main import views

urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^about/$', views.about, name='about'),
    url(r'^contacts/$', views.contacts, name='contacts'),
    url(r'^language/(?P<lang>\w+)$', views.select_lang, name='language'),
    url(r'^search/$', views.search, name='search'),
]
