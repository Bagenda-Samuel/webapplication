from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class UserProfile(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    pp = models.ImageField(upload_to='pp', default="/pp/default.jpg")
    
    def __str__(self):
        return str(self.owner)

class InternshipApplications(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    gender = models.CharField(max_length=10, default = "")
    dob = models.DateField()
    application_letter = models.ImageField(upload_to='letters', default="/letters/default.jpg")
    areas_of_interest = models.TextField()
    university = models.CharField(max_length=100, default = "")
    date_application = models.DateTimeField(default=timezone.now)
    qualified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.owner)

class Gallery(models.Model):
    pic = models.ImageField(upload_to='gallery', default="/gallery/default.jpg", null = True, blank=True)
    figcaption = models.CharField(max_length=300, default = "")

    def __str__(self):
        return str(self.figcaption)