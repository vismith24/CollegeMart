from django.http import HttpResponse
from seller.models import Products_Selling, Category, Products_Leasing
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.conf import settings
from cart.forms import CartAddProductForm
from cart.cart import Cart
from simple_search import search_filter
from django.contrib.auth.models import User
'''
def index(request):
    return render(request, "buyer/home.html")'''


def shop_list(request, rec=0):
    cart = Cart(request)
    categories = Category.objects.all()
    if rec == 0:
        products = Products_Selling.objects.filter(available=True)
    else:
        products = Products_Leasing.objects.filter(available=True)
    paginator = Paginator(products, 12)# Show 12 products per page
    page = request.GET.get('page')
    products = paginator.get_page(page)
    context = {'products':products, 'categories':categories, 'rec':rec, 'cart': cart}
    return render(request, "buyer/shop.html", context)

def shop_category(request, cid, rec=0):
    cart = Cart(request)
    category = Category.objects.get(pk=cid)
    categories = Category.objects.all()
    if rec == 0:
        products_list = Products_Selling.objects.filter(category=category, available=True)
    else:
        products_list = Products_Leasing.objects.filter(category=category, available=True)
    paginator = Paginator(products_list, 12)  # Show 12 products per page
    page = request.GET.get('page')
    products = paginator.get_page(page)
    context = {'products': products , 'categories': categories, 'rec': rec, 'cart': cart}
    return render(request, "buyer/shop-category.html", context)

def shop_item(request, pid, rec):
    cart = Cart(request)
    if rec == 0:
        product = Products_Selling.objects.get(pk=pid)
    else:
        product = Products_Leasing.objects.get(pk=pid)
    cart_product_form = CartAddProductForm()
    context = {'product': product, 'cart_product_form': cart_product_form, 'rec': rec, 'cart': cart}
    return render(request, 'buyer/shop-item.html', context)

def home(request):
    user = User.objects.none()
    if request.user.is_authenticated:
        user = request.user
    cart = Cart(request)
    return render(request, 'buyer/index.html', {'cart': cart, 'user': user})


def about(request):
    return render(request, 'buyer/about.html', {'title': 'About'})

def checkout(request):
    cart = Cart(request)
    return render(request, 'buyer/checkout.html', {'cart': cart})

def search(request):
    if request.method == 'GET':
        search_query = request.GET.get('search_box',None)
        print(search_query)
        if search_query:
            mylist=search_query.split(' ')
            prod_s=Products_Selling.objects.none()
            prod_l=Products_Leasing.objects.none()
            for elements in mylist:
                    search_fields = ['pname', 'description']
                    f = search_filter(search_fields,elements)
                    filtered = Products_Selling.objects.filter(f)
                    if filtered.exists():
                        prod_s=prod_s.union(filtered)
                    search_fields1=['^pname1', 'description1']
                    g=search_filter(search_fields1,elements)
                    filtered1=Products_Leasing.objects.filter(g)
                    if filtered1.exists():
                        prod_l=prod_l.union(filtered1)
            if len(prod_s)!=0 or len(prod_l)!=0:
                return render(request, 'buyer/search.html', {'products': prod_s})
            else:
                return redirect('seller:request')

