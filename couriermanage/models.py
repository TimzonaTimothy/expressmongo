from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.shortcuts import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage


class Courier(models.Model):
	STATUS = (
        ('ON','ON'),
        ('OFF','OFF'),
    )

	tracking_id = models.CharField(max_length=255, null=True)
	sender_name = models.CharField(max_length=255, null=True)
	sender_email = models.CharField(max_length=200,null=True)
	sender_address = models.CharField(max_length=500, blank=True, null=True)
	reciever_name = models.CharField(max_length=250, blank=True, null=True)
	reciever_phone = models.CharField(max_length=200,blank=True, null=True)
	reciever_address = models.CharField(max_length=500, blank=True, null=True)
	reciever_email = models.EmailField(blank=True,null=True)
	origin = models.CharField(max_length=200, blank=True, null=True)
	destination = models.CharField(max_length=300, blank=True, null=True)
	quantity = models.IntegerField(blank=True,null=True)
	content = models.CharField(blank=True, null=True, max_length=255)
	service_type = models.CharField(blank=True, null=True, max_length=255)
	weight = models.CharField(blank=True, null=True, max_length=255)
	departure_time = models.DateTimeField(blank=True,  null=True)
	expected_delivery_date = models.DateTimeField(blank=True, null=True)
	reference = models.CharField(blank=True, null=True, max_length=255)
	status = models.CharField(max_length=20, choices=STATUS, default='OFF',null=True)
	sent = models.BooleanField(default=False)
	list_date = models.DateTimeField(default=timezone.datetime.now, blank = True, null=True)

	def get_absolute_url(self):
		return reverse("couriermanage:listing",args=[self.reference])

	def __str__(self):
		return self.tracking_id
	
	def save(self):
		if self.id:
			old = Courier.objects.get(pk=self.id)
			if old.status == 'ON' and self.sent == False:
				user  = self.reciever_name
				id = self.tracking_id
				mail_subject = 'Shippment Notification'
                
				message = render_to_string('box/shippment.html', {
                    'user' : user,
                    'id':id,
                    })
				to_email = self.reciever_email
				send_email = EmailMessage(mail_subject, message, to=[to_email])
				send_email.content_subtype = "html"
				send_email.send()
				
				self.sent = True
				old.save()
		super(Courier, self).save()

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