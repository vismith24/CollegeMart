from django.urls import path, include
from . import views
from cart import views as cart_views
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

app_name = 'buyer'

urlpatterns = [
    path('about/', views.about, name='about'),
    path('cart/', include('cart.urls')),
    path('payment/', include('paytm.urls')),
    path('shop/<int:rec>', views.shop_list, name='shop'),
    path('shop/<int:rec>/<int:cid>/<int:sid>', views.shop_filters, name='shop-filters'),
    path('shop/<int:cid>/<int:rec>', views.shop_category, name='shop-category'),
    path('shop/item/<int:pid>/<int:rec>', views.shop_item, name='shop-item'),
    path('', views.home, name='home'),
    path('checkout/', views.checkout, name="checkout"),
    path('search/', views.search, name='search'),
    path('order/', views.order_create, name='order'),
    path('order/cancel/<pid>', views.order_cancellation, name='order-cancellation'),
    path('shop/sort_product', views.sort_products, name="sort_product")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)