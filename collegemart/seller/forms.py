from django import forms
from . models import Products_Selling, Products_Leasing

class saleform(forms.ModelForm):

    class Meta:
        model = Products_Selling
        fields = ('pname', 'description','image','category', 'price')

class leaseform(forms.ModelForm):

    class Meta:
        model = Products_Leasing
        fields = ('pname1', 'description1','image1','category1', 'leasing_period')