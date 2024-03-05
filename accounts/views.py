from django.shortcuts import render,redirect
from django.contrib.auth import login,logout,authenticate
from .forms import RegistrationForm,OrderUpdateForm,BrandForm,CarForm
from orders.models import Order,OrderCar
from categories.models import Brand
from cars.models import Car


# Create your views here.
def sign_up(request):
    form = RegistrationForm
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            print(form)
            user = form.save()
            login(request,user)
            return redirect('home')
    return render(request,'accounts/sign-up.html',{'form':form})


def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
    return render(request,'accounts/sign-in.html')


def profile(request):
    if request.user.is_staff:
        return render(request,'accounts/admin_profile.html')
    return render(request,'accounts/dashboard.html')


def sign_out(request):
    logout(request)
    return redirect('home')

def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request,'accounts/order_history.html',{'orders':orders})

def order_details(request,id):
    order = Order.objects.get(id=id)
    order_car = OrderCar.objects.filter(order=order)
    print(order.phone)
    print(order_car)
    total = order.order_total - 500
    return render(request,'accounts/order_details.html',{'order':order,'order_car':order_car,'total':total})

def order_complete(request):
    orders = Order.objects.filter(user=request.user)
    return render(request,'accounts/order_complete.html',{'orders':orders})


def orders_admin(request):
    if request.user.is_staff:
        orders = Order.objects.all()
        return render(request,'accounts/orders_admin.html',{'orders':orders})
    
    
def admin_update(request,id):
    if request.user.is_staff:
        order = Order.objects.get(id=id)
        form = OrderUpdateForm(instance=order)
        if request.method == 'POST':
            form = OrderUpdateForm(request.POST,instance=order)
            if form.is_valid():
                form.save()
                return redirect('admin_orders')
        return render(request,'accounts/update.html',{'form':form})

def brand_view(request):
    if request.user.is_staff:
        brands = Brand.objects.all()
        return render(request,'accounts/brand.html',{'brands':brands})

def brand_upload(request):
    if request.user.is_staff:
        form = BrandForm()
        if request.method == 'POST':
            form = BrandForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                return redirect('brand_view')
        return render(request,'accounts/upload_brand.html',{'form':form})
    
def delete_brand(request,id):
    if request.user.is_staff:
        Brand.objects.get(id=id).delete()
        return redirect('brand_view')
    
def brand_update(request,id):
    if request.user.is_staff:
        brand = Brand.objects.get(id=id)
        form = BrandForm(instance=brand)
        if request.method == 'POST':
            form = BrandForm(request.POST,instance=brand)
            if form.is_valid():
                form.save()
                return redirect('brand_view')
        return render(request,'accounts/update.html',{'form':form})

   
    
def car_view(request):
    if request.user.is_staff:
        cars = Car.objects.all()
        return render(request,'accounts/car.html',{'cars':cars})
    

def car_upload(request):
    if request.user.is_staff:
        form = CarForm()
        if request.method == 'POST':
            form = CarForm(request.POST,request.FILES)
            if form.is_valid():
                form.save()
                return redirect('car_view')
        return render(request,'accounts/upload_car.html',{'form':form})

def delete_car(request,id):
    if request.user.is_staff:
        Car.objects.get(id=id).delete()
        return redirect('car_view')


def car_update(request,id):
    if request.user.is_staff:
        car = Car.objects.get(id=id)
        form = CarForm(instance=car)
        if request.method == 'POST':
            form = CarForm(request.POST,instance=car)
            if form.is_valid():
                form.save()
                return redirect('car_view')
        return render(request,'accounts/update.html',{'form':form})
