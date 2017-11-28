import os

# os.system("echo TEST ITEMS")
# os.system("python manage.py test home.tests.test_items")

os.system("echo TEST JOB VIEW")
os.system("python manage.py test home.tests.test_job_view")

os.system("echo TEST JOBS")
os.system("python manage.py test home.tests.test_jobs")

os.system("echo TEST LOGIN")
os.system("python manage.py test home.tests.test_login")