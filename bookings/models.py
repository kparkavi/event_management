from django.db import models
from django.contrib.auth.models import User
from events.models import Event, TicketType
import uuid

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    
    # Basic Info
    booking_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='bookings')
    ticket_type = models.ForeignKey(TicketType, on_delete=models.CASCADE, related_name='bookings')
    
    # Booking Details
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Attendee Information
    attendee_name = models.CharField(max_length=100)
    attendee_email = models.EmailField()
    attendee_phone = models.CharField(max_length=15)
    special_requirements = models.TextField(blank=True)
    
    # Payment Info
    payment_method = models.CharField(max_length=50, blank=True)
    payment_reference = models.CharField(max_length=100, blank=True)
    
    # Timestamps
    booking_date = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-booking_date']
    
    def __str__(self):
        return f"Booking {self.booking_id} - {self.event.title}"
    
    def save(self, *args, **kwargs):
        if not self.unit_price:
            self.unit_price = self.ticket_type.price
        self.total_amount = self.unit_price * self.quantity
        super().save(*args, **kwargs)
