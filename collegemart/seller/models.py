from django.db import models
from django.urls import reverse


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
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    pname = models.CharField(max_length=100, blank=False, null=False, db_index=True)
    slug = models.SlugField(max_length=100, db_index=True)
    description = models.TextField(blank=False, null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    stock = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='SellingProductsPhotos', blank=False)
    seller = models.ForeignKey("accounts.Profile", on_delete=models.CASCADE)

    class Meta:
        ordering = ('pname', )
        index_together = (('id', 'slug'),)

    def __str__(self):
        return self.pname
    
'''
    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])
'''