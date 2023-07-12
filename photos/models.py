from django.db import models
from cloudinary.models import CloudinaryField
from django.conf import settings
from cloudinary import CloudinaryImage

class Photo(models.Model):
    title = models.CharField(max_length=100)
    image = CloudinaryField('image')
    webp_image = CloudinaryField('image', format='webp',blank=True)
    price = models.IntegerField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='photos', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.title} @ KES {self.price}"
    
    def save(self, *args, **kwargs):
        # Convert the original image to WebP format and save it
        if self.image and not self.webp_image:
            image = CloudinaryImage(self.image)
            webp_version = image.image(transformation={'format': 'webp', 'quality': 'auto'})
            self.webp_image = webp_version.get('url')
        
        super().save(*args, **kwargs)