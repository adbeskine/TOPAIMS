from django.conf.urls import url
from .views import homepage, login, unlock, new_job, jobs, job, new_note, update_job

urlpatterns = [
    url(r'^$', homepage, name='homepage'),
    url(r'^login/$', login, name='login'),
    url(r'^unlock/(?P<unlock_password>.+?)/$', unlock, name='unlock'),
    url(r'^new_job_form/$', new_job, name='new_job_form'),
    url(r'^jobs/$', jobs, name='jobs'),
    url(r'^job/(?P<job_id>.+?)/$', job, name='job'),
    url(r'^new_note/(?P<job_id>.+?)/$', new_note, name='new_note'),
    url(r'^update_job/(?P<job_id>.+?)/(?P<status>.+?)/$', update_job, name='update_job'),
]


