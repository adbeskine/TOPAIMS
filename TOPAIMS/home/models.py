from django.db import models
from datetime import datetime
from django.utils import timezone

class Site_info(models.Model):
	locked = models.BooleanField(default=False) #false when site is locked
	password = models.CharField(max_length=150)

class Jobs(models.Model):
	name = models.CharField(max_length=100, default='')
	email = models.CharField(max_length=100, default='')
	phone = models.CharField(max_length=100, default='')
	address = models.CharField(max_length=100, default='')
	job_id = models.CharField(max_length=100, default='', unique=True)
	status = models.CharField(max_length=100, default='quote')
	# have to manually query notes for all notes whose job foreign key is this job.

class Notes(models.Model):
	Title = models.CharField(max_length=100, default='')
	Text = models.CharField(max_length=100, default='')
	Timestamp = models.DateTimeField(auto_now_add=True)
	job = models.ForeignKey(Jobs, null=True)

	class Meta:
		ordering = ('-Timestamp',)





# Create your models here.
