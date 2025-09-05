from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Booking
from .serializers import BookingCreateSerializer, BookingSerializer
from events.models import Event

class BookingViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = BookingSerializer
    
    def get_queryset(self):
        return Booking.objects.all()

    @action(detail=False, methods=['post'])
    def create_booking(self, request):
        """Create a new booking"""
        event_id = request.data.get('event_id')
        event = get_object_or_404(Event, id=event_id, status='published')
        
        serializer = BookingCreateSerializer(data=request.data)
        if serializer.is_valid():
            booking = serializer.save(user=request.user, event=event)
            return Response(
                BookingSerializer(booking).data,
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        """Confirm a booking"""
        booking = self.get_object()
        if booking.status == 'pending':
            booking.status = 'confirmed'
            booking.save()
            return Response({'message': 'Booking confirmed'})
        return Response(
            {'message': 'Booking cannot be confirmed'},
            status=status.HTTP_400_BAD_REQUEST
        )
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """Cancel a booking"""
        booking = self.get_object()
        if booking.status in ['pending', 'confirmed']:
            booking.status = 'cancelled'
            booking.save()
            return Response({'message': 'Booking cancelled'})
        return Response(
            {'message': 'Booking cannot be cancelled'},
            status=status.HTTP_400_BAD_REQUEST
        )


