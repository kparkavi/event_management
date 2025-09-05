from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Event, TicketType
from django.shortcuts import render

def home(request):
    return render(request, 'pages/home.html')


from .serializers import (
    CategorySerializer, EventListSerializer, EventDetailSerializer,
    EventCreateUpdateSerializer, TicketTypeSerializer
)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = []

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.filter(status='published')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'city', 'is_featured']
    search_fields = ['title', 'description', 'venue']
    ordering_fields = ['start_date', 'created_at', 'title']
    ordering = ['start_date']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return EventListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return EventCreateUpdateSerializer
        return EventDetailSerializer
    
    def get_queryset(self):
        if self.action == 'my_events':
            return Event.objects.filter(organizer=self.request.user)
        return super().get_queryset()
    
    def perform_create(self, serializer):
        serializer.save(organizer=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_events(self, request):
        """Get events created by current user"""
        events = Event.objects.filter(organizer=request.user)
        serializer = EventListSerializer(events, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['get'])
    def tickets(self, request, pk=None):
        """Get ticket types for an event"""
        event = self.get_object()
        tickets = event.ticket_types.all()
        serializer = TicketTypeSerializer(tickets, many=True)
        return Response(serializer.data)

