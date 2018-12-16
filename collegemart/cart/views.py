from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from seller.models import Products_Selling as Product
from seller.models import Products_Leasing as Product2
from .cart import Cart
from .forms import CartAddProductForm
from django.contrib.auth.decorators import login_required

@login_required
@require_POST
def cart_add(request, product_id, rec):
    cart = Cart(request)  # create a new cart object passing it the request object
    rec = int(rec)
    if rec == 0:
        #print('a')
        product = get_object_or_404(Product, id=product_id)
    elif rec:
        #print('b')
        product = get_object_or_404(Product2, id=product_id) 
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, rec=rec, quantity=1, update_quantity=False)
    return redirect('cart:cart_detail')

@login_required
def cart_remove(request, product_id, rec):
    cart = Cart(request)
    rec = int(rec)
    if rec == 0: 
        product = get_object_or_404(Product, id=product_id)
    else:
        product = get_object_or_404(Product2, id=product_id)
    cart.remove(product, rec)
    return redirect('cart:cart_detail')

@login_required
def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantity': item['quantity'], 'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})