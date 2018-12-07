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
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
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
            send_mail(mail_subject, message, "vismith.24.adappa@gmail.com", [to_email])
            return HttpResponse('Please confirm your email address to complete the registration')
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
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')

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
        return render(request, 'accounts/edit_profile.html', {'p_form': p_form})