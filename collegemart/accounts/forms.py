from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from phonenumber_field.formfields import PhoneNumberField
from seller.models import Products_Selling

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    def clean_email(self):
        data = self.cleaned_data['email']
        domain = data.split('@')[1]
        domain_list = ["iiits.in",]
        if domain not in domain_list:
            raise forms.ValidationError("Please enter an Email Address with a valid domain")
        return data
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class ProfileForm(forms.ModelForm):
    fname = forms.CharField(max_length=100, help_text='Required')
    lname = forms.CharField(max_length=100, help_text='Required')
    dob = forms.DateField(help_text='Required')
    phone = PhoneNumberField(help_text='Required')
    photo = forms.ImageField()
    bio = forms.Textarea()

    class Meta:
        model = Profile
        fields = ('fname', 'lname', 'dob', 'phone', 'photo', 'bio')
        widgets = {
            'dob': forms.DateInput(attrs={'class':'dob'}),
        }

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('fname', 'lname', 'dob', 'phone', 'photo', 'bio')
        widgets = {
            'dob': forms.DateInput(attrs={'class': 'dob'}),
        }

class AdminAddProductForm(forms.ModelForm):
    class Meta:
        model = Products_Selling
        fields = ('pname', 'description', 'image', 'category', 'price', 'seller')

class AdminEditUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'is_active')


class AdminEditProductForm(forms.ModelForm):
    class Meta:
        model = Products_Selling
        fields = ('description', 'image', 'category', 'price')