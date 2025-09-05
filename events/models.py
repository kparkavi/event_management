from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    color = models.CharField(max_length=7, default='#007bff')  # Hex color
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.name

class Event(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    
    # Basic Info
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    
    # Event Details
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    venue = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    
    # Capacity & Status
    max_capacity = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    
    # Media
    image = models.ImageField(upload_to='event_images/', blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    @property
    def available_tickets(self):
        confirmed_bookings = self.bookings.filter(status='confirmed').aggregate(
            total=models.Sum('quantity')
        )['total'] or 0
        return self.max_capacity - confirmed_bookings
    
    @property
    def is_full(self):
        return self.available_tickets <= 0

class TicketType(models.Model):
    TICKET_CATEGORIES = [
        ('free', 'Free'),
        ('regular', 'Regular'),
        ('vip', 'VIP'),
        ('early_bird', 'Early Bird'),
        ('student', 'Student'),
    ]
    
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='ticket_types')
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=20, choices=TICKET_CATEGORIES)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity_available = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    
    # Booking limits
    min_quantity = models.PositiveIntegerField(default=1)
    max_quantity = models.PositiveIntegerField(default=10)
    
    def __str__(self):
        return f"{self.event.title} - {self.name}"
    
    @property
    def quantity_sold(self):
        return self.bookings.filter(status='confirmed').aggregate(
            total=models.Sum('quantity')
        )['total'] or 0
    
    @property
    def quantity_remaining(self):
        return self.quantity_available - self.quantity_sold

