from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse

class Courier(models.Model):
	tracking_id = models.CharField(max_length=255, null=True)
	quantity = models.IntegerField(blank=True,null=True)
	content = models.CharField(blank=True, null=True, max_length=255)
	service_type = models.CharField(blank=True, null=True, max_length=255)
	weight = models.CharField(blank=True, null=True, max_length=255)
	reference = models.CharField(blank=True, null=True, max_length=255)
	list_date = models.DateTimeField(default=timezone.datetime.now, blank = True, null=True)

	def get_absolute_url(self):
		return reverse("couriermanage:listing",args=[self.reference])

	def __str__(self):
		return self.tracking_id

class Transaction(models.Model):
	parcel = models.ForeignKey(Courier, on_delete=models.CASCADE)
	activity = models.CharField(max_length=255, null=True, blank=True)
	location = models.CharField(max_length=255, null=True, blank=True)
	details = models.CharField(max_length=225, null=True, blank=True)
	date = models.DateTimeField(default=timezone.datetime.now, blank = True, null=True)

	def __str__(self):
		return  self.activity

	def packacke_date(self):
         return self.date.strftime('%B %d %Y')

class Contact(models.Model):
	first_name = models.CharField(max_length=250,null=True)
	last_name = models.CharField(max_length=250,null=True)
	email = models.CharField(max_length=250,null=True)
	message_subject = models.CharField(max_length=200,null=True)
	message = models.CharField(max_length=500,null=True)
	date_added = models.DateTimeField(auto_now_add=True,null=True)
	
	def __str__(self):
	    return self.email