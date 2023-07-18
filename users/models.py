from datetime import datetime, timedelta
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
import uuid
from .managers import CustomUserManager
from cloudinary.models import CloudinaryField
import jwt

SECRET_KEY = getattr(settings, 'SECRET_KEY', None)

class User(AbstractUser):
    USER_ROLE_CHOICES = (
        ('customer', 'Customer'),
        ('admin', 'Admin'),
    )
    id = models.CharField(max_length=100, unique=True, default=uuid.uuid4, primary_key=True)
    role = models.CharField(max_length=10, choices=USER_ROLE_CHOICES)
    display_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(_("email address"), unique=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    avatar = CloudinaryField('avatar', blank=True, null=True)
    bio = models.CharField(max_length=200, blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = CustomUserManager()

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)
        exp_timestamp = int(dt.timestamp())

        token = jwt.encode({
            'id': str(self.pk),
            'exp': exp_timestamp
        }, SECRET_KEY, algorithm='HS256')
        return token
    
    
    def __str__(self):
        return self.email
    