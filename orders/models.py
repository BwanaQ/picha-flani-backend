from django.db import models
from users.models import User
from photos.models import Photo
from generics.models import Timestamp
from django_fsm import FSMField, transition


class Order(Timestamp):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('REFUNDED', 'Refunded'),
    ]
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, blank=True)
    status = FSMField(default='PENDING',
                      choices=STATUS_CHOICES, null=True, blank=True)
    total_amount = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    # Add other relevant fields for the checkout process

    @transition(field=status, source='PENDING', target='PROCESSING')
    def start_checkout(self):
        pass

    @transition(field=status, source='PROCESSING', target='COMPLETED')
    def complete_checkout(self):
        pass

    @transition(field=status, source=['PENDING', 'PROCESSING'], target='CANCELLED')
    def cancel_checkout(self):
        pass

    @transition(field=status, source='COMPLETED', target='REFUNDED')
    def refund_checkout(self):
        pass

    def __str__(self):
        return f"Order #{self.id}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Photo, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return f"OrderItem #{self.id}"
