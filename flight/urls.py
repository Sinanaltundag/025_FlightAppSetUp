from rest_framework import routers
from django.urls import path
from .views import FlightView, ReservationView

router = routers.DefaultRouter()
router.register('flights', FlightView)
router.register('reservations', ReservationView)

urlpatterns = [
     # path('', include(router.urls)) # This is the default url path for the router.
]
urlpatterns += router.urls