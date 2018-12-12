# Create your tests here.
from django.contrib.auth.models import User
from django.utils import timezone
from django.test import TestCase
from accounts.models import Profile
from .models import Products_Selling,Products_Leasing,Category
from .forms import *
from django.test import Client
from django.urls import reverse


class TestSale(TestCase):
    def create_category(self,category):
        return Category.objects.create(name=category)
    def create_user(self):
        user = User.objects.create(username='Jagan', password='asdfghjkl', email='a@iiits.in')
        return Profile.objects.create(user=user,fname="test",lname="tester",dob="2017-09-23",phone="+919110678098")
    def create_SP(self, pname='Discrete Mathematics', description="yes, this is only a test",price="840.00",):
        return Products_Selling.objects.create(pname=pname, description=description,price=price,
                                               created_at=timezone.now(),category=self.create_category("Hostel"),
                                               seller=self.create_user())

    def test_whatever_creation(self):
        w = self.create_SP()
        self.assertTrue(isinstance(w, Products_Selling))

class TestLease(TestCase):
    def create_category(self,category):
        return Category.objects.create(name=category)
    def create_user(self):
        user = User.objects.create(username='tester', password='asdfghjkl', email='a@iiits.in')
        return Profile.objects.create(user=user,fname="test",lname="tester",dob="2017-09-23",phone="+919110678098")
    def create_LP(self, pname='Discrete Mathematics', description="yes, this is only a test",price="840.00",):
        return Products_Leasing.objects.create(pname1=pname, description1=description,price1=price,
                                               updated_at=timezone.now(),category1=self.create_category("Hostel"),
                                               leaser=self.create_user(),leasing_period="9")

    def test_whatever_creation(self):
        w = self.create_LP()
        self.assertTrue(isinstance(w, Products_Leasing))
