import os


os.system("echo JOB VIEW TEST")
os.system("python manage.py test functional_tests.test_job_view")


os.system("echo LOGIN TEST")
os.system("python manage.py test functional_tests.test_login")

os.system("echo JOBS TEST")
os.system("python manage.py test functional_tests.test_jobs")
