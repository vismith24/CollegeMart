# Create your tests here.
from django.contrib.auth.models import User
from django.utils import timezone
from django.test import TestCase, Client
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

# URL Testing

class UrlTesting(TestCase):
    def setUp(self):
        self.createduser = User.objects.create_user(username="collegemart", email="collegemart@iiits.in",
                                                    password="collegemart123")
        self.client = None
        self.request_url = '/buyer/about/'

    def test_feedback(self):
          self.client=Client()
          response=self.client.get(self.request_url)
          self.assertEqual(response.status_code,200)

    def test_register1(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)


class cartUrlTesting(TestCase):
    def setUp(self):
        self.createduser = User.objects.create_user(username="collegemart", email="collegemart@iiits.in",
                                                    password="collegemart123")
        self.client = None
        self.request_url = '/buyer/cart/'

    def test_feedback(self):
          self.client=Client()
          response=self.client.get(self.request_url)
          self.assertEqual(response.status_code,302)
    def test_register1(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)

class paymentUrlTesting(TestCase):
    def setUp(self):
        self.createduser = User.objects.create_user(username="collegemart", email="collegemart@iiits.in",
                                                    password="collegemart123")
        self.client = None
        self.request_url = '/payment/payment'

    def test_feedback(self):
        self.client=Client()
        response=self.client.get(self.request_url)
        self.assertEqual(response.status_code,301)



class homeUrlTesting(TestCase):
    def setUp(self):
        self.createduser = User.objects.create_user(username="collegemart", email="collegemart@gmail.com",
                                                    password="collegemart123")
        self.client = None
        self.request_url = '/buyer/'

    def test_feedback(self):
          self.client=Client()
          response=self.client.get(self.request_url)
          self.assertEqual(response.status_code,200)

    def test_register1(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)


class checkoutUrlTesting(TestCase):
    def setUp(self):
        self.createduser = User.objects.create_user(username="collegemart", email="collegemart@gmail.com",
                                                    password="collegemart123")
        self.client = None
        self.request_url = '/accounts/reset-password/complete/'


class shopUrlTesting(TestCase):
    def setUp(self):
        self.createduser = User.objects.create_user(username="collegemart", email="collegemart@gmail.com",
                                                    password="collegemart123")
        self.client = None
        self.request_url = '/accounts/reset-password/complete/'


    def test_register1(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)