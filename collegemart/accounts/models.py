from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from collegemart.settings import MEDIA_ROOT

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    fname = models.CharField(max_length=100, blank=False)
    lname = models.CharField(max_length=100, blank=True)
    dob = models.DateField(("DOB"), blank=False)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    rating = models.FloatField(null=False, default=0)
    photo = models.ImageField(upload_to='ProfilePhotos/', null=True, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    email_confirmed = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

    def __repr__(self):
        return self.user.username

    def __unicode__(self):
        return u'Profile of user: %s' % self.user.username