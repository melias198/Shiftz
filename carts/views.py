from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Cart,CartItem
from cars.models import Car

# Create your views here.
def create_session(request):
    if not request.session.session_key:
        request.session.create()
    
    return request.session.session_key


@login_required
def cart(request):
    total = 0
    shipping_fee = 0
    cart_items = None
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(user=request.user)
        for item in cart_items:
            total += item.car.price*item.quantity
    # else:
    #     session_id = create_session(request)
    #     cart = Cart.objects.filter(cart_id=session_id).exists()
    #     if cart:
    #         cart_id = Cart.objects.get(cart_id=session_id) 
    #         cart_items = CartItem.objects.filter(cart=cart_id)
    #         for item in cart_items:
    #             total += item.product.price*item.quantity
    
    if total:
        shipping_fee = 500
    final_total = total+shipping_fee
    return render(request,'carts/cart.html',{'cart_items':cart_items,'fee':shipping_fee,'total':total,'final_total':final_total})


def add_to_cart(request,car_id):
    car = Car.objects.get(id=car_id)
    session_id = create_session(request)
    
    if request.user.is_authenticated:
        cart_id = Cart.objects.filter(cart_id=session_id).exists()
        if cart_id:
            cart_item = CartItem.objects.filter(car=car,user=request.user).exists()
            if cart_item:
                item = CartItem.objects.get(car=car)
                item.quantity += 1
                item.save()
            else:
                cartid = Cart.objects.get(cart_id=session_id)
                cart_item = CartItem.objects.create(
                    user = request.user,
                    car = car,
                    quantity = 1,
                    cart = cartid
                )
                cart_item.save()
        else:
            cart = Cart.objects.create(
                cart_id = session_id
            )
            cart.save()
            
            cartid = Cart.objects.get(cart_id=session_id)
            cart_item = CartItem.objects.create(
                    user = request.user,
                    car = car,
                    quantity = 1,
                    cart = cartid
                )
            cart_item.save()
            
    
    return redirect('cart')


def remove_cart(request,car_id):
    car = Car.objects.get(id=car_id)
    session_id = request.session.session_key
    cart_id = Cart.objects.get(cart_id=session_id)
    
    cart_item = CartItem.objects.get(cart=cart_id,car=car)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
        
    return redirect('cart')

def delete_cart(request,car_id):
    car = Car.objects.get(id=car_id)
    session_id = request.session.session_key
    cart_id = Cart.objects.get(cart_id=session_id)
    print(car_id)
    print(car)
    cart_item = CartItem.objects.get(cart=cart_id,car=car)
    cart_item.delete()
    
    return redirect('cart')