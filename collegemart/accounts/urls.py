from django.conf.urls import url, include
from . import views
from django.urls import path

from django.contrib.auth import views as auth_views

urlpatterns = [
    #url(r'^$', views.index, name='index'),
    # url(r'^account/$', views.account, name='account'),
    # url(r'^login/$', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),

    #path('accounts/', views.accounts, name='accounts'),
    #path('explore/',views.explore,name='explore'),
    #path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    path('login/', views.login, name='login'),
    #path('logout/', views.logout, name='logout'),
    url(r'^logout/$', auth_views.LogoutView.as_view(next_page = '/accounts/login/'), name='logout'),
    url(r'^password/$', views.change_password, name='change_password'),
    url(r'^register/$', views.signup, name='register'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
    url(r'^reset-password/$', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html', email_template_name="accounts/reset_password_email.html", subject_template_name='accounts/password_reset_subject.txt'), name="password_reset"),
    url(r'^reset-password/done/$', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name="password_reset_done"),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"), name="password_reset_confirm"),
    url(r'^reset-password/complete/$', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), name="password_reset_complete"),
    path('admin/user_table/', views.user_show, name='user-show'),
    path('admin/edit_user_select/', views.admin_edit_user_show, name='edit-user-show'),
    path('admin/edit_user/<uid>', views.admin_edit_user, name='admin-edit-user'),
    path('admin/admin_add_user/', views.admin_add_user, name='admin-add-user'),
    path('admin/add_product/', views.admin_add_product, name='admin-add-product'),
    path('admin/product_table/', views.product_show, name='product-show'),
    path('admin/edit_product_select/', views.admin_edit_product_show, name='edit-product-show'),
    path('admin/edit_product/<pid>', views.admin_edit_product, name='admin-edit-product'),
    path('admin/delete_product_select/', views.admin_delete_product_show, name='delete-product-show'),
    path('admin/delete_product/<pid>', views.admin_delete_product, name='admin-delete-product'),
    path('admin/dashboard/',  views.admin_dashboard, name='dashboard'),
    path('admin/order_table/', views.order_show, name='order-show'),
    path('logged_in/', views.logged_in, name='after-login'),
    path('profile/', views.my_profile, name='my-profile'),
    path('edit_my_profile/', views.edit_profile, name='edit-my-profile'),
    path('dashboard/', views.login_dashboard, name='login-dashboard'),
    path('admin/view_invoice_show/', views.admin_invoices_show, name='view-invoice-select'),
    path('admin/view_invoice/<iid>', views.admin_view_invoice, name='admin-view-invoice'),
    path('view_my_invoice/', views.my_invoices_show, name='my-invoices'),
    path('view_invoice/<iid>', views.login_view_invoice, name='view-my-invoice'),
    path('my_orders/',views.myorder, name='my-orders-show'),
    path('my_orders/<pid><n>', views.cancellation, name='my-orders-show'),
    path('admin/requests_show/', views.admin_requests_show, name='admin-requests-show'),
    path('admin/requests_show/<rid>', views.admin_delete_request, name='admin-delete-request'),
    path('view_my_products/', views.view_my_products, name="view-my-products"),
    path('admin/my_profile/', views.admin_profile, name='admin-profile'),
    path('admin/edit_profile/', views.admin_edit_profile, name='admin-edit-profile'),
    path('send_invoice/<oid>', views.Send_Invoice, name='send-invoice-to')
]

