# Create your tests here.
from django.contrib.auth.models import User
from django.utils import timezone
from django.test import TestCase
from accounts.models import Profile
from seller.models import Products_Selling, Products_Leasing,Category
from .models import Orders_Buying, Orders_Leasing


class TestOB(TestCase):
    def create_category(self, category):
        return Category.objects.create(name=category)
    def create_seller(self):
        user = User.objects.create(username='Jagan', password='asdfghjkl', email='a@iiits.in')
        return Profile.objects.create(user=user, fname="test", lname="tester", dob="2017-09-23", phone="+919110678098")

    def create_buyer(self):
        user = User.objects.create(username='Charan', password='qsefthuko', email='b@iiits.in')
        return Profile.objects.create(user=user, fname="test", lname="tester", dob="2017-09-23", phone="+919910678098")

    def create_SP(self, pname='Discrete Mathematics', description="yes, this is only a test",price="840.00",):
        return Products_Selling.objects.create(pname=pname, description=description, price=price,
                                               created_at=timezone.now(), category=self.create_category("Hostel"),
                                               seller=self.create_seller())

    def create_OB(self):
        return Orders_Buying.objects.create(products_selling=self.create_SP(), buyer=self.create_buyer(),
                                                created_at=timezone.now(), isConfirmed = "1")

    def test_whatever_creation(self):
        w = self.create_OB()
        self.assertTrue(isinstance(w, Orders_Buying))


class TestOL(TestCase):
    def create_category(self, category):
        return Category.objects.create(name=category)
    def create_seller(self):
        user = User.objects.create(username='Jagan', password='asdfghjkl', email='a@iiits.in')
        return Profile.objects.create(user=user,fname="test",lname="tester",dob="2017-09-23",phone="+919110678098")

    def create_buyer(self):
        user = User.objects.create(username='Charan', password='qsefthuko', email='b@iiits.in')
        return Profile.objects.create(user=user, fname="test", lname="tester", dob="2017-09-23", phone="+919910678098")

    def create_LP(self, pname='Discrete Mathematics', description="yes, this is only a test",price="840.00",):
        return Products_Leasing.objects.create(pname1=pname, description1=description,price1=price,
                                               updated_at=timezone.now(),category1=self.create_category("Hostel"),
                                               leaser=self.create_seller(),leasing_period="9")

    def create_OL(self):
        return Orders_Leasing.objects.create(products_leasing=self.create_LP(),buyer=self.create_buyer(),
                                                created_at=timezone.now(),isConfirmed = "1")

    def test_whatever_creation(self):
        w = self.create_OL()
        self.assertTrue(isinstance(w, Orders_Leasing))