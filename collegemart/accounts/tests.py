from django.test import TestCase
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
