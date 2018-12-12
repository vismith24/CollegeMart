from django.db import models
from seller.models import Products_Selling
from django.dispatch import receiver
from django.db.models.signals import post_save

BILLING_TYPES = [
        ('1','COD'),
        ('2','ONLINE'),
]

# Create your models here.
class Orders_Buying(models.Model):
    products_selling = models.ForeignKey("seller.Products_Selling", on_delete=models.CASCADE)
    buyer = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    isConfirmed = models.BooleanField(default=True)
    payment_type = models.CharField(max_length=1, default='1', choices=BILLING_TYPES)


class Orders_Leasing(models.Model):
    products_leasing = models.ForeignKey("seller.Products_Leasing", on_delete=models.CASCADE)
    buyer = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    isConfirmed = models.BooleanField(default=True)
    payment_type = models.CharField(max_length=1, default='1', choices=BILLING_TYPES)

class Notification(models.Model):
    message=models.CharField(max_length=100,default="")
    product=models.ForeignKey(Products_Selling,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)


@receiver(post_save,sender=Orders_Buying)
def sendnotification(sender,instance,created,**kwargs):
   if created:
       instance.products_selling.available=False
       instance.products_selling.save()
       message=" Your "+str(instance.products_selling.pname)+" was bought by "+str(instance.buyer.user.username)+" !!"
       Notification.objects.create(
           message=message,
           product=instance.products_selling,
       )
