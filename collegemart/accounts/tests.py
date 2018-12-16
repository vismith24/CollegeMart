from django.test import TestCase, Client
from .models import Profile, User
from .forms import  SignupForm,ProfileForm,ProfileUpdateForm
from django.test import Client
from django.urls import reverse

class TestSignupForm(TestCase):

    def test_SignupForm(self):
        form_instance = SignupForm(data={
            "username": "test_User",
            "email": "mail@iiits.in",
            "password1": "tester321",
            "password2": "tester321",

        })
        self.assertEqual(form_instance.is_valid(), True)

        register = form_instance.save(commit=False)

        register.save()

        model_instance = User.objects.get(username="test_User")
        self.assertEqual(model_instance.username, "test_User")
        self.assertEqual(model_instance.email, "mail@iiits.in")


class RegisterUrlTest(TestCase):

    def setUp(self):
        self.createduser = User.objects.create_user(username="collegemart", email="collegemart@gmail.com",
                                                    password="collegemart123")
        self.client = None
        self.request_url = '/accounts/register/'


    def test_register1(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)



    def test_register(self):
        self.client = Client()
        response = self.client.get(self.request_url)
        self.assertEquals(response.status_code,200)

'''class LogoutUrlTest(TestCase):

    def setUp(self):
        self.createduser = User.objects.create_user(username="collegemart", email="collegemart@gmail.com",
                                                    password="collegemart123")
        self.client = None
        self.request_url = '/accounts/logout/'


    def test_register1(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)



    def test_register(self):
        self.client = Client()
        response = self.client.get(self.request_url)
        self.assertEquals(response.status_code,302)'''
class PasswordUrlTest(TestCase):

    def setUp(self):
        self.createduser = User.objects.create_user(username="collegemart", email="collegemart@gmail.com",
                                                    password="collegemart123")
        self.client = None
        self.request_url = '/accounts/password/'


    def test_register1(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)



    def test_register(self):
        self.client = Client()
        response = self.client.get(self.request_url)
        self.assertEquals(response.status_code,302)
class profileUrlTest(TestCase):

    def setUp(self):
        self.createduser = User.objects.create_user(username="collegemart", email="collegemart@gmail.com",
                                                    password="collegemart123")
        self.client = None
        self.request_url = '/accounts/profile/'



    def test_register(self):
        self.client = Client()
        response = self.client.get(self.request_url)
        self.assertEquals(response.status_code,302)
'''class profileeditUrlTest(TestCase):

    def setUp(self):
        self.createduser = User.objects.create_user(username="collegemart", email="collegemart@gmail.com",
                                                    password="collegemart123")
        self.client = None
        self.request_url = '/accounts/profile/edit/'


    def test_register1(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)



    def test_register(self):
        self.client = Client()
        response = self.client.get(self.request_url)
        self.assertEquals(response.status_code,302)'''
class resetpasswordUrlTest(TestCase):

    def setUp(self):
        self.createduser = User.objects.create_user(username="collegemart", email="collegemart@gmail.com",
                                                    password="collegemart123")
        self.client = None
        self.request_url = '/accounts/reset-password/'


    def test_register1(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)



    def test_register(self):
        self.client = Client()
        response = self.client.get(self.request_url)
        self.assertEquals(response.status_code,200)
class resetdoneUrlTest(TestCase):

    def setUp(self):
        self.createduser = User.objects.create_user(username="collegemart", email="collegemart@gmail.com",
                                                    password="collegemart123")
        self.client = None
        self.request_url = '/accounts/reset-password/done/'


    def test_register1(self):
        self.client = Client()
        self.client.force_login(self.createduser)
        response = self.client.get(self.request_url)
        self.assertEqual(response.status_code, 200)



    def test_register(self):
        self.client = Client()
        response = self.client.get(self.request_url)
        self.assertEquals(response.status_code,200)
class resetcompleteUrlTest(TestCase):

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



    def test_register(self):
        self.client = Client()
        response = self.client.get(self.request_url)
        self.assertEquals(response.status_code,200)











