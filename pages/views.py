from django.shortcuts import render
# Create your views here.
from listings.models import Listing
from doctors.models import Doctor #imported the doctor model from doctors app

def index(request):
    listings = Listing.objects.filter(is_published=True)[:3]
    context = {'listings': listings}
    return render(request, 'pages/index.html', context)

def about(request):
    doctors = Doctor.objects.order_by('-hire_date')[:3]
    mvp_doctors = Doctor.objects.all().filter(is_mvp=True)
    context = {
        'doctors': doctors, 
        'mvp_doctors': mvp_doctors
        }
    return render(request, 'pages/about.html', context)




