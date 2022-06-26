from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from requests import Response
from flight.models import Flight, Reservation
from rest_framework import viewsets
from rest_framework import status

from flight.serializers import FlightSerializer, ReservationSerializer, StaffFlightSerializer
from .permission import IsStaffOrReadOnly
from datetime import datetime, date
from django.db.models import Q

# Create your views here.


class FlightView(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = (IsStaffOrReadOnly,)

    def get_serializer_class(self):
        serializer = super().get_serializer_class()
        if self.request.user.is_staff:
            return StaffFlightSerializer
        return serializer

    def get_queryset(self):
        # queryset = super().get_queryset()
        now = datetime.now()
        current_time = now.strftime('%H:%M:%S')
        today= date.today()

        if self.request.user.is_staff:
            return super().get_queryset()
        else:
            queryset = Flight.objects.filter(Q(date_of_departure__gt=today) | Q(date_of_departure=today, etd__gt=current_time))
            return queryset
       



class ReservationView(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    # permission_classes = (IsStaffOrReadOnly,)

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if ( user and user.is_staff):
            return queryset
        if (user.id):
            private_queryset = get_object_or_404(queryset, user=user)
            return (private_queryset)
        # else:
        #     error_msg = 'pacient error msg'
        #     return {'error': error_msg}
        #     return HttpResponse('That text is invalid')
        #     raise Exception('You are not authorized to view this data')