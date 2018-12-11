from django.db import models

# Create your models here.
class Orders_Buying(models.Model):
    products_selling = models.ForeignKey("seller.Products_Selling", on_delete=models.CASCADE)
    buyer = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    isConfirmed = models.BooleanField(default=True)


class Orders_Leasing(models.Model):
    products_leasing = models.ForeignKey("seller.Products_Leasing", on_delete=models.CASCADE)
    buyer = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    isConfirmed = models.BooleanField(default=True)