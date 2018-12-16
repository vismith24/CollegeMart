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

from InvoiceGenerator.create import create_invoice
from collegemart.settings import MEDIA_ROOT
from accounts.models import Profile
from .models import Orders_Buying, Orders_Leasing

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

import json

'''
def index(request):
    return render(request, "buyer/home.html")'''


def shop_list(request, rec=0):
    cart = Cart(request)
    categories = Category.objects.all()
    if rec == 0:
        products = Products_Selling.objects.filter(available=True).order_by('price')
    else:
        products = Products_Leasing.objects.filter(available=True).order_by('leasing_period')
    paginator = Paginator(products, 12)# Show 12 products per page
    page = request.GET.get('page')
    products = paginator.get_page(page)
    context = {'products':products, 'categories':categories, 'rec':rec, 'cart': cart}
    return render(request, "buyer/shop.html", context)

def shop_filters(request, rec,cid, sid=1):
    category = Category.objects.get(pk=cid)
    c = Category.objects.all()
    products_list = Products_Selling.objects.filter(category=category)
    if(sid==1):
        products_list = Products_Selling.objects.filter(category=category).order_by('price')
    elif(sid==2):
        products_list = Products_Selling.objects.filter(category=category).order_by('-price')
    paginator = Paginator(products_list, 12)  # Show 12 products per page
    page = request.GET.get('page')
    products = paginator.get_page(page)
    context = {'products': products, 'categories': c, 'cid':cid, 'rec': 0, 'category': category}
    return render(request, "buyer/shop-category.html", context)

def shop_category(request, cid, rec=0):
    cart = Cart(request)
    category = Category.objects.get(pk=cid)
    categories = Category.objects.all()
    if rec == 0:
        products_list = Products_Selling.objects.filter(category=category, available=True)
    else:
        products_list = Products_Leasing.objects.filter(category1=category, available=True)
    paginator = Paginator(products_list, 12)  # Show 12 products per page
    page = request.GET.get('page')
    products = paginator.get_page(page)
    context = {'products': products , 'categories': categories,'category': category, 'rec': rec, 'cart': cart}
    return render(request, "buyer/shop-category.html", context)

@login_required
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

@login_required
def checkout(request):
    cart = Cart(request)
    return render(request, 'buyer/checkout.html', {'cart': cart})

@login_required
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
        return redirect('buyer:home')

@login_required
def order_create(request):
    if request.method == 'POST':
        mode = request.POST['mode']
        if mode == '1':
            cart = Cart(request)
            profile = Profile.objects.get(user=request.user)
            for item in cart:
                rec = int(item['rec'])
                if rec == 0:
                    order = Orders_Buying.objects.create(products_selling = item['sproduct'], buyer = profile, payment_type=mode)
                    p = Products_Selling.objects.filter(id = item['sproduct'].id)[0]
                    p.available = False
                    p.save()
                else:
                    Orders_Leasing.objects.create(products_leasing = item['lproduct'], buyer = profile, payment_type=mode)
                    p = Products_Leasing.objects.filter(id = item['lproduct'].id)[0]
                    p.available = False
                    p.save()
                profile = Profile.objects.get(user = request.user)
                create_invoice(profile, order)
                current_site = get_current_site(request)
                mail_subject = 'Your Order Invoice.'
                message = render_to_string('buyer/order_email.html')
                to_email = request.user.email
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                email.attach_file(MEDIA_ROOT+'/orders/'+str(order.id)+".pdf")
                email.send()
            return redirect('buyer:home')
        else:
            cart = Cart(request)
            profile = Profile.objects.get(user=request.user)
            for item in cart:
                rec = int(item['rec'])
                if rec == 0:
                    order = Orders_Buying.objects.create(products_selling = item['sproduct'], buyer = profile, payment_type=mode)
                    p = Products_Selling.objects.filter(id = item['sproduct'].id)[0]
                    p.available = False
                    p.save()
                else:
                    Orders_Leasing.objects.create(products_leasing = item['lproduct'], buyer = profile, payment_type=mode)
                    p = Products_Leasing.objects.filter(id = item['lproduct'].id)[0]
                    p.available = False
                    p.save()
                profile = Profile.objects.get(user = request.user)
                create_invoice(profile, order)
                current_site = get_current_site(request)
                mail_subject = 'Your Order Invoice.'
                message = render_to_string('buyer/order_email.html')
                to_email = request.user.email
                email = EmailMessage(
                            mail_subject, message, to=[to_email]
                )
                email.attach_file(MEDIA_ROOT+'/orders/'+str(order.id)+".pdf")
                email.send()
            return redirect('paytm:payment')

@login_required
def order_cancellation(request, pid):
    o=Orders_Buying.objects.get(pk=pid)
    p = o.products_selling
    p.available = True
    p.save()
    message=" The order for "+str(o.products_selling.pname)+" has been cancelled by "+str(o.buyer.user.username)+" !!"
    Notification.objects.create(
        message=message,
        product=p,
    )
    o.delete()
    return redirect('buyer:home')

def sort_products(request):
    if request.method == 'GET':
        sort_text = request.POST.get('filter')
        response_data = {}
        
        if sort_text == '1':
            p = Products_Selling.objects.filter().order_by('price')
        else:
            p = Products_Selling.objects.filter().order_by('-price')
            v = list(p.values())
            k = []
            count = 0
            for c in v:
                k.append({})
                for key,value in c.items():
                    if key == 'id' or key == 'pname'or key == 'rating':
                        k[count][key] = value
                    elif key == 'price':
                        k[count][key] = str(value)
                count += 1
        response_data['products'] = k
        return HttpResponse(json.dumps(response_data), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"nothing to see": "this isn't happening"}), content_type="application/json")
