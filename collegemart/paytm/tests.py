from django.test import TestCase,Client
from django.contrib.auth.models import User
class UrlTesting(TestCase):
    def setUp(self):
        self.client = Client()
        u = User.objects.create(username='a', password='asdfghjkl', email='a@b.com')
        return u

    def test_paytm(self):
        self.client=Client()
        response=self.client.get('/payment/payment/')
        print(response.status_code)
        res2 = self.client.get('/payment/response/')
        print(res2.status_code)
        res3 = self.client.get('/payment/status/')
        self.assertEqual(response.status_code,200)


