from django.conf.urls import url
from .views import homepage, login, unlock, new_job, job

urlpatterns = [
    url(r'^$', homepage, name='homepage'),
    url(r'^login/$', login, name='login'),
    url(r'^unlock/(?P<unlock_password>.+?)/$', unlock, name='unlock'),
    url(r'^new_job_form/$', new_job, name='new_job_form'),
    url(r'^job/(?P<job_id>.+?)/$', job, name='job'),
]