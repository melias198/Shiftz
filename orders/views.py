from django.shortcuts import render,redirect
from carts.models import Cart,CartItem
from .forms import OrderForm
from datetime import datetime
from .ssl import sslcommerz_payment_gateway
from .models import Payment, OrderCar, Order
from cars.models import Car
from .ssl import sslcommerz_payment_gateway
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


# Create your views here.
@method_decorator(csrf_exempt, name='dispatch') 
def success_view(request):
    data = request.POST
    user_id = int(data['value_b'])  
    user = User.objects.get(pk=user_id)
    payment = Payment(
        user = user,
        payment_id =data['tran_id'],
        payment_method = data['card_issuer'],
        amount_paid = int(data['store_amount'][0]),
        status =data['status'],
    )
    payment.save()
    
    
    order = Order.objects.get(user=user, is_ordered=False, order_number=data['value_a'])
    order.payment = payment
    order.is_ordered = True
    order.save()
    cart_items = CartItem.objects.filter(user = user)
    
    for item in cart_items:
        ordercar = OrderCar()
        car = Car.objects.get(id=item.car.id)
        ordercar.order = order
        ordercar.payment = payment
        ordercar.user = user
        ordercar.car = car
        ordercar.quantity = item.quantity
        ordercar.ordered = True
        ordercar.save()

        
        
        car.stock -= item.quantity 
        car.save()

    
    CartItem.objects.filter(user=user).delete()
    return redirect('cart')
    
def checkout(request):
    cart_items = None
    total = 0
    grand_total = 0
    current_date = datetime.now().date()
    formatted_date = current_date.strftime("%Y%m%d")
    cart_items = CartItem.objects.filter(user = request.user)
    
    if cart_items.count() < 1:
        return redirect('store')
    
    for item in cart_items:
        total += item.car.price * item.quantity
        
    shipping_fee = 500  
    grand_total = total + shipping_fee
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.order_total = grand_total
            form.instance.ip = request.META.get('REMOTE_ADDR')
            form.instance.payment = 2
            saved_instance = form.save()  
            form.instance.order_number = formatted_date+str(saved_instance.id)
            
            form.save()
            
            # return redirect(sslcommerz_payment_gateway(request,  saved_instance.id, str(request.user.id), grand_total))
            # Try
            payment = Payment(
                user = request.user,
                payment_id = 'TXN',
                payment_method = 'Cash',
                amount_paid = grand_total,
                status = 'Success'
            )
            payment.save()
            
            order = Order.objects.get(user=request.user,is_ordered=False)
            order.payment = payment
            order.is_ordered = True
            order.save()
            cart_items = CartItem.objects.filter(user=request.user)
            
            for item in cart_items:
                ordercar = OrderCar()
                car = Car.objects.get(id=item.car.id)
                ordercar.order = order
                ordercar.payment = payment
                ordercar.user = request.user
                ordercar.car = car
                ordercar.quantity = item.quantity
                ordercar.ordered = True
                ordercar.save()
                
                car.stock -= item.quantity
                car.save()
            
            CartItem.objects.filter(user=request.user).delete()
            return redirect('order_complete')
                

    return render(request, 'orders/place-order.html',{'cart_items' : cart_items,'fee':shipping_fee, 'total' : total, 'final_total' : grand_total})


def order_complete(request):
    return render(request,'orders/order_complete.html')


