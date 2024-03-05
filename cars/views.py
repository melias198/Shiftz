from django.shortcuts import render
from .models import Car
from categories.models import Brand
from .forms import CarFilterForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.
def cars(request,brand_slug=None):
    cars =None
    brands = None
    search_query = None
    
    if request.method == 'POST':
        search_query = request.POST.get('search_query', '') 
        cars = Car.objects.filter(car_name__icontains=search_query) 
        
        form = CarFilterForm(request.POST)
        
        if form.is_valid() and not search_query:
            brand_slug = form.cleaned_data.get('brand_filter')
            model_slug = form.cleaned_data.get('model_filter')
    
            if brand_slug:
                brand = get_object_or_404(Brand,slug=brand_slug)
            else:
                brand = None
            
            query = Q(is_available=True)
            if brand:
                query &= Q(brand=brand)
            if model_slug:
                query &= Q(slug=model_slug)

            cars = Car.objects.filter(query)
            
    else:
        brands = Brand.objects.all()
        cars = Car.objects.all()
        form = CarFilterForm()
        
    page = request.GET.get('page')
    paginator = Paginator(cars, 3)
    page_obj = paginator.get_page(page)
    
    context = {'cars':page_obj,'brands':brands,'form':form,'search_query':search_query}
        
    return render(request,'cars/car.html',context)


def car_details(request,brand_slug,car_slug):
    cars = Car.objects.get(slug=car_slug,brand__slug=brand_slug)
    return render(request,'cars/car-details.html',{'cars':cars})