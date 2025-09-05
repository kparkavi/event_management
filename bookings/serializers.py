from rest_framework import serializers
from .models import Booking
from events.serializers import EventListSerializer, TicketTypeSerializer

class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            'ticket_type', 'quantity', 'attendee_name',
            'attendee_email', 'attendee_phone', 'special_requirements'
        ]
    
    def validate(self, attrs):
        ticket_type = attrs['ticket_type']
        quantity = attrs['quantity']
        
        # Check quantity limits
        if quantity < ticket_type.min_quantity:
            raise serializers.ValidationError(f"Minimum quantity is {ticket_type.min_quantity}")
        
        if quantity > ticket_type.max_quantity:
            raise serializers.ValidationError(f"Maximum quantity is {ticket_type.max_quantity}")
        
        # Check availability
        if quantity > ticket_type.quantity_remaining:
            raise serializers.ValidationError(f"Only {ticket_type.quantity_remaining} tickets available")
        
        return attrs

class BookingSerializer(serializers.ModelSerializer):
    event = EventListSerializer(read_only=True)
    ticket_type = TicketTypeSerializer(read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'booking_id', 'event', 'ticket_type', 'quantity',
            'unit_price', 'total_amount', 'status', 'attendee_name',
            'attendee_email', 'attendee_phone', 'booking_date', 'confirmed_at'
        ]

