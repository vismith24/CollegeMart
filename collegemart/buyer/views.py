from django.http import HttpResponse
from seller.models import Products_Selling, Category, Products_Leasing
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.conf import settings
from cart.forms import CartAddProductForm
from cart.cart import Cart

'''
def index(request):
    return render(request, "buyer/home.html")'''


def shop_list(request, rec=0):
    categories = Category.objects.all()
    if rec == 0:
        products = Products_Selling.objects.filter(available=True)
    else:
        products = Products_Leasing.objects.filter(available=True)
    paginator = Paginator(products, 12)# Show 12 products per page
    page = request.GET.get('page')
    products = paginator.get_page(page)
    context = {'products':products, 'categories':categories, 'rec':rec }
    return render(request, "buyer/shop.html", context)

def shop_category(request, cid, rec=0):
    category = Category.objects.get(pk=cid)
    categories = Category.objects.all()
    if rec == 0:
        products_list = Products_Selling.objects.filter(category=category, available=True)
    else:
        products_list = Products_Leasing.objects.filter(category=category, available=True)
    paginator = Paginator(products_list, 12)  # Show 12 products per page
    page = request.GET.get('page')
    products = paginator.get_page(page)
    context = {'products': products , 'categories': categories, 'rec': rec}
    return render(request, "buyer/shop-category.html", context)

def shop_item(request, pid, rec):
    if rec == 0:
        product = Products_Selling.objects.get(pk=pid)
    else:
        product = Products_Leasing.objects.get(pk=pid)
    cart_product_form = CartAddProductForm()
    context = {'product': product, 'cart_product_form': cart_product_form, 'rec': rec}
    return render(request, 'buyer/shop-item.html', context)

def home(request):
    return render(request, 'buyer/index.html')


def about(request):
    return render(request, 'buyer/about.html', {'title': 'About'})

def checkout(request):
    cart = Cart(request)
    return render(request, 'buyer/checkout.html', {'cart': cart})

