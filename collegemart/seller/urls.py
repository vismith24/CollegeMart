from django.urls import path,include
from django.conf.urls import url
from . import views

app_name = 'seller'

urlpatterns=[
    path('',views.productsale,name="saleform.home"),
    path('sale/',views.tosell,name="tosell"),
    path('sale/<pid><n>', views.deletion, name="tosell"),
    path('request/', views.Request, name="request"),
]