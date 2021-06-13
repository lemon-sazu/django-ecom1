from store.models import OrderItem, Order, Product, ShippingAddress
from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .utils import *
# Create your views here.


def store(request):
    product = Product.objects.all()
    data = cartData(request)
    cartItem = data['cartItems']

    context = {
        'products': product,
        'cartItem': cartItem
    }
    return render(request, 'store/store.html', context)


def cart(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItem = data['cartItems']

    context = {'items': items, 'order': order, 'cartItem': cartItem}
    return render(request, 'store/cart.html', context)


def checkout(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItem = data['cartItems']

    context = {'items': items, 'order': order, 'cartItem': cartItem}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Product Id: ', productId)
    print('Action: ', action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    # order = Order.objects.create(
    #     customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item Was Added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.get(
            customer=customer, complete=False)

        # order, created = Order.objects.get_or_create(
        #     customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])

    order.transaction_id = transaction_id

    if total == float(order.get_cart_total):
        order.complete = True
    order.save()

    if order.shipping == True:
        ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipode=data['shipping']['zipcode'],
        )

    return JsonResponse("Payment Completed", safe=False)
