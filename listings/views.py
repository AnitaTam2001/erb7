from django.shortcuts import render
from .models import Listing
# Create your views here.
def listings(request):
    listings = Listing.objects.all() 
    print("listing data")
    print(listings)
    #use listing select *.  objects.all = queryset 
    context = {'listings': listings} 
    #listings = base manager. 
    return render(request, 'listings/listings.html', context)

def listing(request):
    return render(request, 'listings/listing.html')

def search(request):
    return render(request, 'listings/search.html')

