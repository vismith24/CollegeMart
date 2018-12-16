from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save


class Category(models.Model):
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=150, unique=True ,db_index=True)

    class Meta:
        ordering = ('name', )
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
'''
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])
'''

class Products_Selling(models.Model):
    category = models.ForeignKey(Category, related_name='products_selling', on_delete=models.CASCADE)
    pname = models.CharField(max_length=100, blank=False, null=False, db_index=True)
#    slug = models.SlugField(max_length=100, db_index=True)
    description = models.TextField(blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    stock = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    rating = models.FloatField(null=False, default=0)
    image = models.ImageField(upload_to='SellingProductsPhotos', blank=False)
    seller = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
 
    def __str__(self):
        return self.pname
    
'''
    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
'''

class Products_Leasing(models.Model):
    category1 = models.ForeignKey(Category, related_name='products_leasing', on_delete=models.CASCADE)
    pname1 = models.CharField(max_length=100, blank=False, null=False, db_index=True)
#    slug = models.SlugField(max_length=100, db_index=True)
    description1 = models.TextField(blank=False, null=False)
    price1 = models.DecimalField(max_digits=10, decimal_places=2, default=50)
    stock = models.PositiveIntegerField(default=1)
    updated_at = models.DateTimeField(auto_now=True)
    available = models.BooleanField(default=True)
    rating = models.FloatField(null=False, default=0)
    image1 = models.ImageField(upload_to='LeasingProductsPhotos', blank=False)
    leaser = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)
    leasing_period = models.IntegerField(null=False, blank=False)
    start_date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.pname1

class Request_table(models.Model):
    pname2 = models.CharField(max_length=100, blank=False, null=False)
    description2 = models.TextField(blank=False, null=False)
    person = models.ForeignKey('accounts.Profile', on_delete=models.CASCADE)
    def __str__(self):
        return self.pname2

    def __repr__(self):
        return self.pname2

class commonNotification(models.Model):
    message=models.CharField(max_length=100,default="")
    request=models.ForeignKey(Request_table,on_delete=models.CASCADE,default='')
    status=models.BooleanField(default=False)


@receiver(post_save,sender=Request_table)
def sendnotification(sender,instance,created,**kwargs):

   if created:
       message=" One of your collegemates needs "+str(instance.pname2)+".If you have it, you can post an ad."
       commonNotification.objects.create(
           message=message,
           request=instance
       )

