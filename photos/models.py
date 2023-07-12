from django.db import models
from cloudinary.models import CloudinaryField
# import user model
from django.conf import settings
class Photo(models.Model):
    title = models.CharField(max_length=100)
    image = CloudinaryField('image')
    price = models.IntegerField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='photos', on_delete=models.CASCADE)
    def __str__(self) -> str:
        return f"{self.title} @ KES {self.price}"