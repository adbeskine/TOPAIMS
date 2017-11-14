from django.db import models

class Site_info(models.Model):
	locked = models.BooleanField(default=False) #false when site is locked
	password = models.CharField(max_length=150)

class Notes(models.Model):
	Title = models.CharField(max_length=100, default='')
	Text = models.CharField(max_length=100, default='')

class Jobs(models.Model):
	name = models.CharField(max_length=100, default='')
	email = models.CharField(max_length=100, default='')
	phone = models.CharField(max_length=100, default='')
	address = models.CharField(max_length=100, default='')
	job_id = models.CharField(max_length=100, default='')
	notes = models.ForeignKey(Notes, on_delete=models.CASCADE, default='')



# Create your models here.
