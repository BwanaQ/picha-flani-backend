import uuid
from django.db import models
from users.models import User
from generics.models import Timestamp
from django_fsm import FSMField, transition


class Transaction(Timestamp):
    id = models.CharField(max_length=100, unique=True, default=uuid.uuid4, primary_key=True)
    buyer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='purchases', null=True, blank=True)
    amount = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    reference_number = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=12, null=True, blank=True)
    payment_method = models.CharField(max_length=50, null=True, blank=True)

    state = FSMField(default='pending', choices=[
        ('PENDING', 'Pending'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
        ('REFUNDED', 'Refunded'),
    ])

    @transition(field=state, source='PENDING', target='COMPLETED')
    def complete(self):
        # Add logic for transitioning to the 'completed' state
        pass

    @transition(field=state, source='PENDING', target='CANCELLED')
    def cancel(self):
        # Add logic for transitioning to the 'cancelled' state
        pass

    @transition(field=state, source='*', target='REFUNDED')
    def refund(self):
        # Add logic for transitioning to the 'refunded' state
        pass

    def __str__(self):
        return f"Transaction #{self.id}"
