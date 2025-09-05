from rest_framework import serializers
from .models import Category, Event, TicketType
from accounts.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'color', 'created_at']

class TicketTypeSerializer(serializers.ModelSerializer):
    quantity_sold = serializers.ReadOnlyField()
    quantity_remaining = serializers.ReadOnlyField()
    
    class Meta:
        model = TicketType
        fields = [
            'id', 'name', 'category', 'price', 'quantity_available',
            'quantity_sold', 'quantity_remaining', 'description',
            'min_quantity', 'max_quantity'
        ]

class EventListSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    available_tickets = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'organizer', 'category',
            'start_date', 'end_date', 'venue', 'city',
            'max_capacity', 'available_tickets', 'is_full',
            'status', 'is_featured', 'image', 'created_at'
        ]

class EventDetailSerializer(serializers.ModelSerializer):
    organizer = UserSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    ticket_types = TicketTypeSerializer(many=True, read_only=True)
    available_tickets = serializers.ReadOnlyField()
    is_full = serializers.ReadOnlyField()
    
    class Meta:
        model = Event
        fields = [
            'id', 'title', 'slug', 'description', 'organizer', 'category',
            'start_date', 'end_date', 'venue', 'address', 'city',
            'max_capacity', 'available_tickets', 'is_full',
            'status', 'is_featured', 'image', 'ticket_types',
            'created_at', 'updated_at'
        ]

class EventCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = [
            'title', 'slug', 'description', 'category',
            'start_date', 'end_date', 'venue', 'address', 'city',
            'max_capacity', 'status', 'is_featured', 'image'
        ]