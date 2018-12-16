from django.http import HttpResponse
from django.shortcuts import render, redirect
from .forms import SignupForm, ProfileForm, ProfileUpdateForm
from django.contrib.auth.forms import PasswordChangeForm
from .models import Profile
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.core.mail import send_mail, EmailMessage
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import update_session_auth_hash

from accounts.models import Profile
from seller.models import Products_Selling, Request_table, Products_Leasing
from buyer.models import Orders_Buying, Orders_Leasing
from .forms import AdminAddProductForm, AdminEditUserForm, AdminEditProductForm

from seller.models import commonNotification
from buyer.models import Notification, Leasing_Notification

from django.urls import reverse

from cart.cart import Cart
from collegemart.settings import MEDIA_ROOT
# Create your views here.

def signup(request):
    if request.method == 'POST':
        form1 = SignupForm(request.POST)
        form2 = ProfileForm(request.POST, request.FILES)
        if form1.is_valid() and form2.is_valid():
            user = form1.save(commit=False)
            user.is_active = True
            user.save()
            profile = form2.save(commit=False)
            profile.user = user
            profile.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your CollegeMart Account.'
            message = render_to_string('accounts/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form1.cleaned_data.get('email')
        send_mail(mail_subject, message, "collegemart.ase1@gmail.com", [to_email])    
        return redirect('login')
    else:
        form1 = SignupForm()
        form2 = ProfileForm()
        return render(request, 'accounts/register.html', {'form1': form1, 'form2': form2,})

        

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.profile.email_confirmed=True
        user.save()
        login(request, user)
        #return redirect('accounts:accounts')
        return redirect('login')
    else:
        return redirect('login')

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('view_profile')  
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'accounts/change_password.html', {'form': form})

def login(request):
    cart = Cart(request)
    cart.cart.clear()
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            print(user)
            auth_login(request, user)
            u = User.objects.get(username=user)
            print(u)
            if u.is_superuser:
                return redirect('dashboard')
            else:
                return redirect('my-profile')
        else:
            return redirect('login')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

@login_required
def view_profile(request):
    context = {'user': request.user}
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'Your account has been updated successfully!')
            return redirect('logout')
        profile = Profile.objects.get(user=request.user)
        p_form = ProfileUpdateForm(instance=profile)
    else:
        p_form = ProfileUpdateForm(instance=profile)
        u = User.objects.get(username=request.user)
        profile = Profile.objects.get(user=request.user)
        return render(request, 'my template/login_edit_profile.html', {'p_form': p_form, 'profile': profile, 'u': u})

def admin_dashboard(request):
    products = Products_Selling.objects.all().count()
    users = User.objects.all().count()
    orders = Orders_Buying.objects.all().count()
    return render(request, 'my template/admin_dashboard.html', {'products': products, 'users': users, 'orders': orders})

def user_show(request):
    user = User.objects.all()
    return render(request, 'my template/demo_table.html', {'user':user})

def admin_add_product(request):
    if request.method == 'POST':
        form3 = AdminAddProductForm(request.POST, request.FILES)
        if form3.is_valid():
            product = form3.save()
            m = Products_Selling.objects.filter(seller=product.seller)
            return render(request, 'my template/admin_my_products.html', {'m': m})
    else:
        form3 = AdminAddProductForm()
        return render(request, 'my template/admin_add_product_form.html', {'form3': form3})

def admin_my_products(request):
    m = Products_Selling.objects.all()
    return render(request, 'my template/admin_my_products.html', {'m': m})

@login_required
def view_my_products(request):
    p = Profile.objects.get(user=request.user)
    m = Products_Selling.objects.filter(seller=p)
    n = Products_Leasing.objects.filter(leaser=p)
    return render(request, 'my template/login_my_products.html', {'m': m, 'profile': p, 'n': n})

@login_required
def my_profile(request):
    u = User.objects.get(username=request.user)
    if u.is_superuser:
        return render(request, 'my template/admin_profile.html',{ 'u': u})
    profile = Profile.objects.get(user=request.user)
    return render(request, 'my template/login_profile.html', {'profile': profile, 'u': u})

def product_show(request):
    product = Products_Selling.objects.all()
    return render(request, 'my template/admin_products_table.html', {'product':product})


def admin_add_user(request):
    if request.method == 'POST':
        form1 = SignupForm(request.POST)
        if form1.is_valid():
            user = form1.save(commit=False)
            user.is_active = False
            user.save()
            return redirect('/accounts/admin/user_table/')
    else:
        form1 = SignupForm()
    return render(request, 'my template/admin_add_user.html', {'form1': form1})


def admin_edit_user_show(request):
    user = User.objects.all()
    return render(request, 'my template/admin_edit_user.html', {'user': user})


def admin_edit_user(request, uid):
    if request.method == 'POST':
        # uid = u.pk
        user = User.objects.get(pk=uid)
        form7 = AdminEditUserForm(request.POST)
        if form7.is_valid():
            form7 = AdminEditUserForm(request.POST, instance=user)
            form7.save()
            return redirect('edit-user-show')
    else:
        user = User.objects.get(pk=uid)
        form7 = AdminEditUserForm(instance=user)
    return render(request, 'my template/admin_edit_user_form.html', {'form7': form7, 'user': user})


def admin_edit_product_show(request):
    product = Products_Selling.objects.all()
    return render(request, 'my template/admin_edit_product.html', {'product': product})


def admin_edit_product(request, pid):
    if request.method == 'POST':
        product = Products_Selling.objects.get(pk=pid)
        form8 = AdminEditProductForm(request.POST,request.FILES)
        if form8.is_valid():
            form8 = AdminEditProductForm(request.POST, instance=product)
            form8.save()
            return redirect('edit-product-show')
    else:
        product = Products_Selling.objects.get(pk=pid)
        form8 = AdminEditProductForm(instance=product)
    return render(request, 'my template/admin_edit_product_form.html', {'form8': form8, 'product': product})


def admin_delete_product_show(request):
    product = Products_Selling.objects.all()
    return render(request, 'my template/admin_delete_product.html', {'product': product})

def admin_delete_product(request, pid):
    product = Products_Selling.objects.get(pk=pid)
    product.delete()
    return redirect('delete-product-show')

def order_show(request):
    order = Orders_Buying.objects.all()
    return render(request, 'my template/admin_order_show.html', {'order': order})

def logged_in(request):
    return render(request, 'my template/login_base.html')

@login_required
def login_dashboard(request):
    profile = Profile.objects.get(user=request.user)
    u = User.objects.get(username=request.user)

    # for notifications
    cn = commonNotification.objects.all()
    cn_count = commonNotification.objects.all().count()

    n = reversed(Notification.objects.filter(product__seller__user = request.user))
    n_count = Notification.objects.filter(product__seller__user = request.user).count()

    l = reversed(Leasing_Notification.objects.filter(product__leaser__user = request.user))
    l_c = Leasing_Notification.objects.filter(product__leaser__user = request.user).count()

    #Notification.seller.Products_Selling.Seller.user.username

    return render(request, 'my template/login_dashboard.html', {'profile': profile, 'cn': cn, 'cn_count': cn_count, 'n': n, 'n_count': n_count, 'l_c': l_c, 'l': l})

def admin_invoices_show(request):
    order = Orders_Buying.objects.all()
    return render(request, 'my template/admin_invoice_show.html', {'order': order})


def admin_view_invoice(request, iid):
    order = Orders_Buying.objects.get(pk=iid)
    seller = User.objects.get(username=order.products_selling.seller)
    seller_profile = Profile.objects.get(user__username=order.products_selling.seller)

    print(seller)
    print(seller_profile)
    return render(request, 'my template/admin_view_invoice.html', {'order': order, 'seller': seller, 'seller_profile': seller_profile})

@login_required
def my_invoices_show(request):
    p = Profile.objects.get(user=request.user)
    order = Orders_Buying.objects.filter(buyer=p)
    return render(request, 'my template/login_my_invoices_show.html', {'order': order, 'profile': p})

@login_required
def login_view_invoice(request, iid):
    order = Orders_Buying.objects.get(pk=iid)
    seller = User.objects.get(username=order.products_selling.seller)
    seller_profile = Profile.objects.get(user__username=order.products_selling.seller)
    profile  = Profile.objects.get(user = request.user)

    return render(request, 'my template/login_view_invoice.html', {'order': order, 'seller': seller, 'seller_profile': seller_profile, 'profile': profile})

@login_required
def myorder(request):
    p = Profile.objects.get(user=request.user)
    m = Orders_Buying.objects.filter(buyer=p)
    n = Orders_Leasing.objects.filter(buyer=p)
    return render(request, 'my template/login_my_orders.html', {'m': m,'n':n})

@login_required
def cancellation(request,pid,n):
    if n=='0':
        o=Orders_Buying.objects.get(pk=pid)
        p = o.products_selling
        p.available=True
        p.save()
        message=" The order for "+str(o.products_selling.pname)+" has been cancelled by "+str(o.buyer.user.username)+" !!"
        Notification.objects.create(
            message=message,
            product=p,
        )
        o.delete()
    else:
        o = Orders_Leasing.objects.get(pk=pid)
        p = o.products_leasing
        p.available = True
        p.save()
        message = " The order for " + str(o.products_leasing.pname1) + " has been cancelled by " + str(
            o.buyer.user.username) + " !!"
        Leasing_Notification.objects.create(
            message=message,
            product=p,
        )
        o.delete()
    return redirect('my-orders-show')

def admin_requests_show(request):
    r_requests = Request_table.objects.all()
    return render(request, 'my template/admin_requests_show.html', {'r_requests': r_requests})

def admin_delete_request(request,rid):
    r = Request_table.objects.get(pk=rid)
    r.delete()
    return redirect('admin-requests-show')

def admin_profile(request):
    u = User.objects.get(username=request.user)
    profile = Profile.objects.get(user=request.user)
    return render(request, 'my template/admin_profile.html', {'profile': profile, 'u': u})

def admin_edit_profile(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)

        if p_form.is_valid():
            p_form.save()
            messages.success(request, f'Your account has been updated successfully!')
            return redirect('logout')
        profile = Profile.objects.get(user=request.user)
        p_form = ProfileUpdateForm(instance=profile)
    else:
        p_form = ProfileUpdateForm(instance=profile)
        u = User.objects.get(username=request.user)
        profile = Profile.objects.get(user=request.user)
        return render(request, 'my template/admin_edit_profile.html', {'p_form': p_form, 'profile': profile, 'u': u})

def Send_Invoice(request,oid):
    mail_subject = 'Your Order Invoice.'
    message = render_to_string('buyer/order_email.html')
    to_email = request.user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.attach_file(MEDIA_ROOT + '/orders/' + str(oid) + ".pdf")
    email.send()
    print('email sent!!!!!')
    return redirect('view-invoice-select')