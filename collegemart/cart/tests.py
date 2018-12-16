from django.test import TestCase,Client
from django.urls import reverse
from django.contrib.auth.models import User

from seller.models import Products_Selling, Category

from accounts.models import Profile
from .models import *


class UrlTesting(TestCase):

    def setUp(self):
        self.client = None
        self.request_url = '/cart/'

    def test_feedback(self):
        self.client=Client()
        response=self.client.get(self.request_url)
        #response=self.client.get(url)
        self.assertEqual(response.status_code, 200)

