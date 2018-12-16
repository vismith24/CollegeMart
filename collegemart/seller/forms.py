from django import forms
from . models import Products_Selling, Products_Leasing, Request_table

class saleform(forms.ModelForm):

    class Meta:
        model = Products_Selling
        fields = ('pname', 'description','image','category', 'price')

class leaseform(forms.ModelForm):

    class Meta:
        model = Products_Leasing
        fields = ('pname1', 'description1','image1','category1', 'leasing_period')

class requestform(forms.ModelForm):

    class Meta:
        model = Request_table
        fields = ('pname2','description2')