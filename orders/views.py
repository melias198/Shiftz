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
@csrf_exempt
def success_view(request):
    data = request.POST
    user_id = int(data['value_b'])  
    user = User.objects.get(pk=user_id)
    print(user)
    print(data['value_a'])
    or_id = data['value_a']
    payment = Payment(
        user = user,
        payment_id =data['tran_id'],
        payment_method = data['card_issuer'],
        amount_paid = float(data['store_amount']), 
        status =data['status'],
    )
    payment.save()
    
    # working with order model
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

        # Reduce the quantity of the sold products
        car.stock -= item.quantity 
        car.save()

    # Clear cart
    CartItem.objects.filter(user=user).delete()
    
    # Invoice Details
    order_details = Order.objects.get(user=user,order_number=or_id)
    payment_details = Payment.objects.get(user=user,payment_id=order_details.payment.payment_id)
    car_details = OrderCar.objects.filter(user=user,payment=payment_details)
    
    product_price = 0
    for i in car_details:
        product_price += i.car.price*i.quantity
    
    total_price =product_price+500
    context = {'order_details':order_details,'payment_details':payment_details,'product_details':car_details,'product_price':product_price,'total_price':total_price}
    return render(request,'orders/order_complete.html',context)


@csrf_exempt
def faild_view(request):
    template_name = 'orders/faild_order.html'
    if request.method == 'GET':
        return render(request, template_name)
    elif request.method == 'POST':
        return render(request, template_name)

    
def checkout(request):
    cart_items = None
    total = 0
    shipping_fee = 0
    # grand_total = 0
    current_date = datetime.now().date()
    formatted_date = current_date.strftime("%Y%m%d")
    
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user = request.user)
        if cart_items.count() < 1:
            return redirect('store')
        for item in cart_items:
            total += item.car.price * item.quantity
    else:
        return redirect('login')
    
    
    if total: 
        shipping_fee = 500  
    grand_total = total + shipping_fee
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.instance.user = request.user
            form.instance.order_total = grand_total
            form.instance.ip = request.META.get('REMOTE_ADDR')
            saved_instance = form.save()  
            form.instance.order_number = formatted_date+str(saved_instance.id)
            form.save()
            ord_id = form.instance.order_number
            return redirect(sslcommerz_payment_gateway(request,  ord_id, str(request.user.id), grand_total))
            
    return render(request, 'orders/place-order.html',{'cart_items' : cart_items,'fee':shipping_fee, 'total' : total, 'final_total' : grand_total})


def order_complete(request):
    return render(request,'orders/order_complete.html')


def user_order_track(request,id):
    order = Order.objects.get(id=id)
    orderstatus = Order.STATUS
    return render(request, 'orders/order_traking.html',{'order':order,'orderstatus':orderstatus})


