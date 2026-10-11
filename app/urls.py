from django.contrib import admin
from django.urls import path
from .models import *
from .views import *

urlpatterns = [
    path('chome/',customer_home,name="chome"),
    path('signin/',register,name="signin"),
    path('login/',user_login,name="login"),
    path('logout/',user_logout,name="logout"),
    path('bookrides/',book_ride,name="book_rides"),
    path('myrides/',customer_rides,name="myride"),
    path('dhome/',driver_home,name="dhome"),
    path('available/',available_rides,name="available"),
    path("available-rides/",available_rides,name="available_rides"),
    path("ride/<int:ride_id>/accept/",accept_ride,name="accept_ride"),
    path("ride/<int:ride_id>/cancel/",cancel_ride,name="cancel_ride"),
]