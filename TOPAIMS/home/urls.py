from django.conf.urls import url
from .views import homepage, login

urlpatterns = [
    url(r'^$', homepage, name='homepage'),
    url(r'^login/$', login, name='login'),
]