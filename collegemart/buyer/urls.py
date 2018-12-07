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
    path('shop/', views.shop_list, name='shop'),
    path('shop/<int:cid>', views.shop_category, name='shop-category'),
    path('shop/item/<int:pid>', views.shop_item, name='shop-item'),
    path('', views.home, name='home'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)