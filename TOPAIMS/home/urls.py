from django.conf.urls import url
from .views import homepage, login, unlock

urlpatterns = [
    url(r'^$', homepage, name='homepage'),
    url(r'^login/$', login, name='login'),
    url(r'^unlock/(?P<unlock_password>.+?)/$', unlock, name='unlock'),
]