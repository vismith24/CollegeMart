from functools import reduce
from django.shortcuts import render,redirect, render_to_response
from django.template import RequestContext
from . models import Products_Selling, Products_Leasing
from accounts.models import Profile
from . forms import saleform, leaseform, requestform
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from simple_search import search_filter
from django.urls import reverse

# Create your views here.

@login_required()
def productsale(request):
    profile = Profile.objects.filter(user=request.user)[0]
    if request.method == 'POST':
        form3=saleform(request.POST, request.FILES)
        form5=leaseform(request.POST, request.FILES)
        if form3.is_valid():
            p = Profile.objects.filter(user=request.user)[0]
            product = form3.save(commit=False)
            product.seller = p
            product.save()
            return redirect('buyer:home')
        if form5.is_valid():
            p = Profile.objects.filter(user=request.user)[0]
            product = form5.save(commit=False)
            product.leaser = p
            product.save()
            return redirect('buyer:home')
        else:
            form3 = saleform()
            form5 = leaseform()
            return render(request, 'seller/saleform.html', {'form3': form3,'form5':form5, 'profile': profile})
        return redirect('buyer:home')    
    else:
        form3 = saleform()
        form5 = leaseform()
        return render(request, 'seller/saleform.html', {'form3': form3,'form5':form5, 'profile': profile})


@login_required()
def tosell(request):
    p = Profile.objects.get(user=request.user)
    m = Products_Selling.objects.filter(seller=p)
    n = Products_Leasing.objects.filter(leaser=p)
    if request.method == 'GET':
        search_query = request.GET.get('search_box',None)
        print(search_query)
        if search_query:
            mylist=search_query.split(' ')
            inst=[]
            for elements in mylist:
                    search_fields = ['^pname', 'description']
                    f = search_filter(search_fields,elements)
                    filtered = Products_Selling.objects.filter(f)
                    if filtered.exists():
                        inst.append(filtered)
                    else:
                        return render(request, 'seller/tosell.html', {'m': m,'n':n})
            return render(request, 'seller/search.html', {'inst': inst})
        else:
            return render(request, 'seller/tosell.html', {'m': m,'n':n})
    else:
        return render(request, 'seller/tosell.html', {'m': m,'n':n})

def deletion(request,pid,n='0'):
    if n=='0':
        a=Products_Selling.objects.filter(pk=pid)
        a.delete()
    else:
        a = Products_Leasing.objects.filter(pk=pid)
        a.delete()
    return redirect('view-my-products')

def Request(request):
    p = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form7 = requestform(request.POST)
        if form7.is_valid():
            p = Profile.objects.filter(user=request.user)[0]
            product = form7.save(commit=False)
            product.person = p
            print(product.person)
            product.save()
            return redirect('seller:saleform.home')
        else:
            form7=requestform()
            return render(request, 'seller/request.html', {'form7':form7, 'profile': p})
    else:
        form7 = requestform()
        return render(request, 'seller/request.html', {'form7': form7, 'profile': p})