from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    picture = models.ImageField(upload_to='profile_images', blank=True)

    def __str__(self):
        return self.user.username


class Stay(models.Model):
    name = models.CharField(max_length=128, unique=True)
#    stayID = models.CharField(max_length=30, unique=True)
#    picture = models.ImageField(upload_to=None)
    price = models.IntegerField(default=0)
    propertyRating = models.DecimalField(max_digits=3, decimal_places=1, default=0.0)
    description = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    longitude = models.DecimalField(max_digits=15, decimal_places=10, default=0)
    contacts = models.CharField(max_length=100)

    postedBy = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Stay, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Review(models.Model):
    stay = models.ForeignKey(Stay, on_delete=models.CASCADE)
    title = models.CharField(max_length=128, default='Review')
    impression = models.IntegerField(default=0)
    locationRating = models.IntegerField(default=0)
    cleanliness = models.IntegerField(default=0)
    descripAccuracy = models.IntegerField(default=0)
    costRating = models.IntegerField(default=0)
    comment = models.CharField(max_length=255)

    reviewedBy = models.ForeignKey(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
