from django.contrib import admin
from .models import Category, Event, TicketType

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'color', 'created_at']
    search_fields = ['name']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'organizer', 'category', 'start_date', 'status', 'max_capacity']
    list_filter = ['status', 'category', 'is_featured', 'city']
    search_fields = ['title', 'description', 'venue']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(TicketType)
class TicketTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'event', 'category', 'price', 'quantity_available']
    list_filter = ['category']
