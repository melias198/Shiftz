from django.shortcuts import render,redirect,reverse
from django.contrib.auth import login,logout,authenticate
from .forms import RegistrationForm,OrderUpdateForm,BrandForm,CarForm,UpdateForm,OrderStatusForm
from orders.models import Order,OrderCar,Payment
from categories.models import Brand
from cars.models import Car
from django.contrib import messages

from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail
from .models import OtpToken

# Create your views here.
# def sign_up(request):
#     form = RegistrationForm()
#     if request.method == 'POST':
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             # user.is_active = False  
#             user.backend = 'django.contrib.auth.backends.ModelBackend' # specify 
#             user.save()
#             login(request,user)
#             return redirect('home')
#     return render(request,'accounts/sign-up.html',{'form':form})


def sign_up(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  
            user.backend = 'django.contrib.auth.backends.ModelBackend' # specify 
            user.save()
            # login(request,user)
            # return redirect('home')
            messages.success(request, "Account created successfully! An OTP was sent to your Email")
            return redirect("verify-email", username=request.POST['username'])
    return render(request,'accounts/sign-up.html',{'form':form})


# OTP Verify
def verify_email(request, username):
    user = get_user_model().objects.get(username=username)
    print(user)
    user_otp = OtpToken.objects.filter(user=user).last()
    
    if request.method == 'POST':
        if user_otp.otp_code == request.POST['otp_code']:
            
            # checking for expired token
            if user_otp.otp_expires_at > timezone.now():
                user.is_active=True
                user.backend = 'django.contrib.auth.backends.ModelBackend'
                user.save()
                messages.success(request, "Account activated successfully!! You can Login.")
                return redirect("login")
            # expired token
            else:
                messages.warning(request, "The OTP has expired, get a new OTP!")
                return redirect("verify-email", username=user.username)
        
        # invalid otp code
        else:
            messages.warning(request, "Invalid OTP entered, enter a valid OTP!")
            return redirect("verify-email", username=user.username)
        
    context = {}
    return render(request, "verify_email/verify_token.html", context)


def resend_otp(request):
    if request.method == 'POST':
        user_email = request.POST["otp_email"]
        
        if get_user_model().objects.filter(email=user_email).exists():
            user = get_user_model().objects.get(email=user_email)
            otp = OtpToken.objects.create(user=user, otp_expires_at=timezone.now() + timezone.timedelta(minutes=5))
            
            # email variables
            subject="Email Verification"
            message = f"""
                                Hi {user.username}, here is your OTP {otp.otp_code} 
                                it expires in 5 minute, use the url below to redirect back to the website
                                https://shiftz.onrender.com/account/verify-email/{user.username}
                                
                                """
            sender = "shiftzcars@gmail.com"
            receiver = [user.email, ]
        
        
            # send email
            send_mail(
                    subject,
                    message,
                    sender,
                    receiver,
                    fail_silently=False,
                )
            
            messages.success(request, "A new OTP has been sent to your email-address")
            return redirect("verify-email", username=user.username)

        else:
            messages.warning(request, "This email dosen't exist in the database")
            return redirect("resend-otp")
        
    context = {}
    return render(request, "verify_email/resend_otp.html", context)




def sign_in(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password')
            return render(request, 'accounts/sign-in.html')
    return render(request,'accounts/sign-in.html')


def profile(request):
    if request.user.is_staff:
        return render(request,'accounts/admin_profile.html')
    return render(request,'accounts/dashboard.html')


def profile_update(request):
    user = request.user
    form = UpdateForm(instance=user)
    if request.method == 'POST':
        form = UpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    return render(request,'accounts/update.html',{'form':form})


def sign_out(request):
    logout(request)
    return redirect('home')

def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request,'accounts/order_history.html',{'orders':orders})


def track_order(request):
    orders = Order.objects.filter(user=request.user)
    return render(request,'accounts/order_track.html',{'orders':orders})



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


def transaction_history(request):
    transactions = Payment.objects.filter(user=request.user)
    return render(request,'accounts/transaction.html',{'transactions':transactions})


def transaction_details(request,id):
    order_obj = Order.objects.get(payment__id=id)
    print(order_obj.id)
    return redirect(reverse('order_details', args=[order_obj.id]))


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
    

def update_status(request,id):
    if request.user.is_staff:
        order = Order.objects.get(id=id)
        form = OrderStatusForm(instance=order)
        if request.method == 'POST':
            form = OrderStatusForm(request.POST,instance=order)
            if form.is_valid():
                form.save()
                return redirect('admin_orders')
        return render(request,'accounts/update.html',{'form':form})


def admin_order_details(request,id):
    order = Order.objects.get(id=id)
    order_car = OrderCar.objects.filter(order=order)
    total = order.order_total - 500
    return render(request,'accounts/admin_order_details.html',{'order':order,'order_car':order_car,'total':total})

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
