from django.db import models

# Create your models here.

class Task (models.Model):

	id = models.AutoField(primary_key=True,max_length=20)
	taskid = models.CharField(null=True,max_length=40,default='1')
	name = models.CharField(null=True,max_length=100)
	mathod = models.CharField(null=False,max_length=2,default='a')
	java = models.CharField(null=False,max_length=2,default='1')
	other = models.CharField(null=False,max_length=1024,default='nothing')
	filepath = models.CharField(null=False,max_length=100,default='no')
	datetime = models.CharField(null=False,max_length=100)

	class Meta:
		db_table = 'Task'
		ordering = ['id']

class Result (models.Model):

	id = models.AutoField(primary_key=True)
	taskid = models.CharField(null=False,max_length=64,default='1')
	issue = models.CharField(null=False,max_length=1024,default='1')
	desc = models.CharField(null=False,max_length=1024,default='1')
	title = models.CharField(null=False,max_length=64,default='1')
	level = models.CharField(null=False,max_length=2,default='1') #0,1,2,3 info,low,mid,high
	filepath = models.CharField(null=False,max_length=128,default='1')
	line = models.CharField(null=False,max_length=64,default='1')
	content = models.CharField(null=False,max_length=1024,default='1')

	class Meta:
		db_table = 'Result'
		ordering = ['id']



