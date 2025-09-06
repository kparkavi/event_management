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
    payment_reference = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Auto-generated payment reference"
    )
    
    # Timestamps
    booking_date = models.DateTimeField(auto_now_add=True)
    confirmed_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-booking_date']
    
    def __str__(self):
        return f"Booking {self.booking_id} - {self.event.title}"
    
    def generate_payment_reference(self):
        """Generate a unique payment reference"""
        return f"PAY-{self.booking_id.hex[:8].upper()}-{uuid.uuid4().hex[:4].upper()}"
    
    def save(self, *args, **kwargs):
        # Set unit price from ticket type if not provided
        if not self.unit_price:
            self.unit_price = self.ticket_type.price
        
        # Calculate total amount
        self.total_amount = self.unit_price * self.quantity
        
        # Generate payment reference if not exists
        if not self.payment_reference:
            # Save first to get the booking_id
            super().save(*args, **kwargs)
            self.payment_reference = self.generate_payment_reference()
            # Save again with payment reference
            super().save(update_fields=['payment_reference'])
        else:
            super().save(*args, **kwargs)

            