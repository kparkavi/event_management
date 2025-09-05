from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_id', 'user', 'event', 'quantity', 'total_amount', 'status', 'booking_date']
    list_filter = ['status', 'booking_date']
    search_fields = ['booking_id', 'user__username', 'event__title']
    readonly_fields = ['booking_id', 'total_amount']


