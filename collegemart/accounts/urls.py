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
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='accounts/homepage.html'), name='logout'),
    url(r'^password/$', views.change_password, name='change_password'),
    url(r'^register/$', views.signup, name='register'),
    url(r'^profile/$', views.view_profile, name='view_profile'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate, name='activate'),
    url(r'^reset-password/$', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html', email_template_name="accounts/reset_password_email.html", subject_template_name='accounts/password_reset_subject.txt'), name="password_reset"),
    url(r'^reset-password/done/$', auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'), name="password_reset_done"),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"), name="password_reset_confirm"),
    url(r'^reset-password/complete/$', auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_complete.html"), name="password_reset_complete"),
]

