from rest_framework import serializers
from .models import Flight, Passenger, Reservation


class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flight
        fields = (
            'id',
            'flight_number', 
            'operation_airlines', 
            'departure_city', 
            'arrival_city', 
            'date_of_departure', 
            'etd',
            )


class PassengerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Passenger
        fields = '__all__'
        

class ReservationSerializer(serializers.ModelSerializer):

    passenger = PassengerSerializer(many=True, required=False)
    flight = serializers.StringRelatedField()
    user = serializers.StringRelatedField()
    flight_id = serializers.IntegerField(write_only=True)
    user_id = serializers.IntegerField(write_only=True, required=False)
    class Meta:
        model = Reservation
        fields = (
            'id',
            'user',
            'passenger',
            'flight',
            'flight_id',
            'user_id',
            )

    def create(self, validated_data):
        passenger_data = validated_data.pop('passenger')
        validated_data['user_id'] = self.context['request'].user.id
        reservation = Reservation.objects.create(**validated_data)
        for passenger in passenger_data:
            # Passenger.objects.create(reservation=reservation, **passenger)
            pas = Passenger.objects.create(**passenger)
            reservation.passenger.add(pas)
        reservation.save()
        return reservation

class StaffFlightSerializer(serializers.ModelSerializer):

    reservations = ReservationSerializer(many=True, read_only=True)
    
    class Meta:
        model = Flight
        fields = (
                'id',
                'flight_number', 
                'operation_airlines', 
                'departure_city', 
                'arrival_city', 
                'date_of_departure', 
                'etd',
                'reservations',
                )
    
    