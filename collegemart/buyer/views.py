from django.http import HttpResponse
from seller.models import Products_Selling, Category
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


def shop_list(request):
    categories = Category.objects.all()
    products = Products_Selling.objects.all()
    paginator = Paginator(products, 12)# Show 12 products per page
    page = request.GET.get('page')
    products = paginator.get_page(page)
    context = {'products':products, 'categories':categories }
    return render(request, "buyer/shop.html", context)


def shop_category(request, cid):
    category = Category.objects.get(pk=cid)
    categories = Category.objects.all()
    products_list = Products_Selling.objects.filter(category=category)
    paginator = Paginator(products_list, 12)  # Show 12 products per page
    page = request.GET.get('page')
    products = paginator.get_page(page)
    context = {'products': products , 'categories': categories}
    return render(request, "buyer/shop-category.html", context)

def shop_item(request, pid):
    product = Products_Selling.objects.get(pk=pid)
    cart_product_form = CartAddProductForm()
    context = {'product': product, 'cart_product_form': cart_product_form}
    return render(request, 'buyer/shop-item.html', context)

def home(request):
    products = Products_Selling.objects.all()[0:6]
    categories = Category.objects.all()
    context = {'products': products, 'categories': categories}
    return render(request, 'buyer/index.html', context)


def about(request):
    return render(request, 'buyer/about.html', {'title': 'About'})

def checkout(request):
    cart = Cart(request)
    return render(request, 'buyer/checkout.html', {'cart': cart})

