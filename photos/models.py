from django.db import models
from cloudinary.models import CloudinaryField
# import user model
from django.contrib.auth.models import User
class Photo(models.Model):
    title = models.CharField(max_length=100)
    image = CloudinaryField('image')
    price = models.IntegerField()
    owner = models.ForeignKey('auth.User', related_name='photos', on_delete=models.CASCADE)
    def __str__(self) -> str:
        return f"{self.title} @ KES {self.price}"