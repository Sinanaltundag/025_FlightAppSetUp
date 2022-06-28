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
    passenger_id= serializers.IntegerField(required=False, write_only=True)
    class Meta:
        model = Passenger
        fields = ("id", "first_name", "last_name", "email", "phone_number", "passenger_id")
        

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
            passenger.pop("passenger_id")
            pas = Passenger.objects.create(**passenger)
            reservation.passenger.add(pas)
        reservation.save()
        return reservation

    # def create(self, validated_data):
    #     passenger_data = validated_data.pop('passenger')

    #     validated_data['user_id'] = self.context['request'].user.id
    #     reservation = Reservation.objects.create(**validated_data)
    #     for passenger in passenger_data:
    #         if "id" in passenger.keys():
    #             pas = Passenger.objects.get(id=passenger["id"])
    #             reservation.passenger.add(pas)
    #         else:
    #             pas = Passenger.objects.create(**passenger)
    #             reservation.passenger.add(pas)
    #     reservation.save()
    #     return reservation


    # def update(self, instance, validated_data):
        
    #     passenger_data = validated_data.pop('passenger')
    #     mevcut = instance.passenger.all()

    #     #update yapılırken yolcu silmek için
    #     mevcutIdlist=[Id.id for Id in mevcut ]
    #     updatedIdlist= [item["id"] for item in passenger_data if "id" in item.keys()]
    #     for Id in mevcutIdlist:
    #         if Id in updatedIdlist:
    #             pass
    #         else:
    #             print("yok", Id)
    #             mevcut = mevcut.exclude(id=Id)
    #     instance.passenger.set(mevcut)
    #     # print(instance.passenger.all())
      
    #     #update yaperken var olan yolcuları güncellemek, olmayanları creat etmek için
    #     for  passenger in passenger_data:
    #         #gelen bilgilerde yolcu id si var mı? var ise bu id mevcut rezervasyonda mı yoksa var olan diğer yolcular arasında mı
    #         if "id" in passenger.keys():
    #             pas = mevcut.filter(id=passenger["id"])
    #             if pas:
    #                 pas = pas.update(**passenger)
    #             else:
    #                 pas = Passenger.objects.get(id=passenger["id"])
    #                 instance.passenger.add(pas)
    #         else: 
    #                 pas = Passenger.objects.create(**passenger)
    #                 print(pas)
    #                 instance.passenger.add(pas)

    def update(self, instance, validated_data):
        passenger_data = validated_data.pop('passenger')
        instance.user_id = self.context['request'].user.id
        instance.save()

        for passenger in passenger_data:
            # if passenger['passenger_id'] is not None:
            if "passenger_id" in passenger.keys():
                pas = Passenger.objects.get(id=passenger['passenger_id'])
                pas.first_name = passenger['first_name']
                pas.last_name = passenger['last_name']
                pas.email = passenger['email']
                pas.phone_number = passenger['phone_number']
                pas.save()
                instance.passenger.add(pas)
            else:
                pass
                pas = Passenger.objects.create(**passenger)
                instance.passenger.add(pas)
            # pas = Passenger.objects.create(**passenger)
        instance.save()
        return instance

    # def updateUser(self, instance, validated_data):
    #     passenger_data = validated_data.pop('passenger')
    #     instance.user_id = self.context['request'].user.id
    #     instance.save()
    #     for passenger in passenger_data:
    #         # Passenger.objects.create(reservation=reservation, **passenger)
    #         pas = Passenger.objects.create(**passenger)
    #         instance.passenger.add(pas)
    #     instance.save()
    #     return instance   


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
    
    