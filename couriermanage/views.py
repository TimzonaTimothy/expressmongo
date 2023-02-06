from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.generic import ListView
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required
from .models import Courier
from django.contrib import messages
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from .models import *

def home(request):
	
	return render(request, 'box/index.html', {})

def search(request):
	
	couriers = Courier.objects.filter()
	
	query = request.GET.get('q')
	if query:
		couriers = Courier.objects.filter(tracking_id=query)
			
	Couriers = Courier.objects.order_by('-list_date')
	paginator = Paginator(couriers, 10)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	return render(request,'box/search.html', {'page_obj':page_obj})



def listing(request, id=None):

    listing = get_object_or_404(Courier, id=id)
    
    
    # transaction = get_object_or_404(Transaction, parcel=listing.id)
    t = Transaction.objects.all().filter(parcel=listing.id)
    context = {
        'listing':listing,
		'transactions':t,
		}

    return render(request, 'box/listing.html', context)

def about(request):
	return render(request, 'box/about.html', {})

def services(request):
	return render(request, 'box/service.html', {})

def sea_freight(request):
	return render(request, 'box/sea-freight.html', {})

def air_freight(request):
	return render(request, 'box/air-freight.html', {})

def land_freight(request):
	return render(request, 'box/land-freight.html', {})

def warehouse(request):
	return render(request, 'box/warehouse.html', {})

def custom_clearance(request):
	return render(request, 'box/custom-clearance.html', {})

def contact(request):
	if request.method == "POST":
		massage_firstname = request.POST['firstname'] 
		massage_lastname = request.POST['lastname'] 
		massage_email = request.POST['email']
		massage_subject = request.POST['massage_subject']
		massage = request.POST['message']
            #send mai
            
		contact = Contact.objects.create(first_name=massage_firstname,last_name=massage_lastname,email=massage_email,message_subject=massage_subject,message=massage)
		contact.save();
		messages.success(request, 'Your massage has been submitted ','alert alert-success alert-dismissible')
		# send_mail(
		# 	massage_firstname + ''+ massage_lastname +' sent you an enquiry '+ massage_email + ' '+ massage_subject,
		# 	massage,
		# 	'arizonatymothy@gmail.com',
		# 	['arizonatymothy@gmail.com',],
		# 	fail_silently=False
		# 	)
		# messages.success(request, 'Your email has been sent ','alert alert-success alert-dismissible')
		return render(request, 'box/contact.html', {})
	else:
		return render(request, 'box/contact.html', {})


def track(request):
	return render(request, 'box/tracking.html', {})




def sign_in(request):
	if request.user.is_authenticated:
		return redirect('home')
	
	else:
			
		if request.method == 'POST':
			username = request.POST['Username']
			password = request.POST['Password']

			user = auth.authenticate(username=username, password=password)

			if user is not None:
				auth.login(request,user)
				messages.success(request, 'Login Success')
				return HttpResponseRedirect(reverse('main')) 
			else:
				messages.error(request, 'Invalid credentials')
				return redirect('/login')
		else:
			return render(request, 'log/login.html',{})
		


def register(request):
	if request.user.is_authenticated:
		return redirect('home')
    
   
	else:

		if request.method == 'POST':
			first_name = request.POST['firstname']
			last_name = request.POST['lastname']
			username = request.POST['username']
			email = request.POST['email']
			password = request.POST['password1']
			password2 = request.POST['password2']
		

			if password==password2:
				if User.objects.filter(email=email).exists():
					messages.warning(request, 'Email Taken')
					return redirect('/register')
				elif User.objects.filter(username=username).exists():
					messages.warning(request, 'Username Taken')
					return redirect('/register')
				else:
					user = User.objects.create_user(username=username, email=email, password=password,first_name=first_name,last_name=last_name,)
					user.save();
					messages.success(request, 'You are now registered and can log in')
					print('user created')
					return redirect('/login')

			else:
				messages.warning(request, 'Password Not Matching')
				return HttpResponseRedirect('/register')
			return HttpResponseRedirect('/register')

		else:
			return render(request, 'log/register.html', {})


  
	


@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))
