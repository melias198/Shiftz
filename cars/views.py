from django.shortcuts import render
from .models import Car
from categories.models import Brand
from .forms import CarFilterForm
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.
def cars(request):
    brands = Brand.objects.all()
    cars = Car.objects.all()
    form = CarFilterForm()
        
    page = request.GET.get('page')
    paginator = Paginator(cars, 3)
    page_obj = paginator.get_page(page)
    
    context = {'cars':page_obj,'brands':brands,'form':form}
    return render(request,'cars/car.html',context)


def search_view(request):
    if request.method == 'GET':
        search_query = request.GET.get('search_query', '')
        cars = Car.objects.filter(car_name__icontains=search_query)
        brands = Brand.objects.all()
        form = CarFilterForm()
    
    page = request.GET.get('page')
    paginator = Paginator(cars, 3)
    page_obj = paginator.get_page(page)
    total = len(cars)
    
    context = {'cars':page_obj,'brands':brands,'form':form,'search_query':search_query,'total':total}
    return render(request,'cars/search.html',context)


def filter_view(request):
    if request.method == 'GET':
        form = CarFilterForm(request.GET)
        if form.is_valid():
            brand_filter = form.cleaned_data.get('brand')
            model_filter = form.cleaned_data.get('model')
            
        brands = Brand.objects.all()
            
        query = Q(is_available=True)
        if brand_filter:
            query &= Q(brand__slug=brand_filter)
        if model_filter:
            query &= Q(slug=model_filter)

        cars = Car.objects.filter(query)
    
    page = request.GET.get('page')
    paginator = Paginator(cars, 3)
    page_obj = paginator.get_page(page)
    total = len(cars)
    
    context = {'cars':page_obj,'brands':brands,'form':form,'brand':brand_filter,'model':model_filter,'total':total}
    return render(request,'cars/filter.html',context)



def car_details(request,brand_slug,car_slug):
    cars = Car.objects.get(slug=car_slug,brand__slug=brand_slug)
    return render(request,'cars/car-details.html',{'cars':cars})