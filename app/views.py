from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate
from .models import *

def customer_home(request):
    return render(request,"chome.html")

def register(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request,
                "register.html",
                {
                    "error":"User already exists."
                }
            )

        user=User.objects.create_user(
            username=username,
            password=password
        )

        Profile.objects.create(
            user=user,
            role=request.POST['role']
        )

        return redirect("login")
    return render(request,"register.html")

def user_login(request):

    if request.method == "POST":

        user = authenticate(
            username=request.POST['username'],
            password=request.POST['password']
        )

        if user is not None:

            login(request, user)

            profile = Profile.objects.get(user=user)

            if profile.role == "DRIVER":
                return redirect("dhome")
            else:
                return redirect("chome")

        else:

            return render(
                request,
                "login.html",
                {
                    "error": "Invalid Username or Password."
                }
            )

    return render(request, "login.html")

def user_logout(request):
    logout(request)
    return redirect("login")

def driver_home(request):
    return render(request,"dhome.html")

@login_required
def book_ride(request):

    if request.method == "POST":

        pickup = request.POST['pickup']
        drop = request.POST['drop']

        if "calculate" in request.POST:

            if pickup == drop:

                return render(request,
                    "book_rides.html",
                    {
                        "error": "The source and destination should not be same"
                    }
                )

            route = Route.objects.filter(
                source=pickup,
                destination=drop
            ).first()

            if route is None:

                return render(request,
                    "book_rides.html",
                    {
                        "error": "There is No Route Available"
                    }
                )

            distance = route.distance

            fare = distance * 20

            return render(request,
                "fare.html",
                {
                    "pickup": pickup,
                    "drop": drop,
                    "distance": distance,
                    "fare": fare
                }
            )

        if "book" in request.POST:

            distance = request.POST['distance']

            fare = request.POST['fare']

            Ride.objects.create(
                customer=request.user,
                pickup_location=pickup,
                drop_location=drop,
                distance=distance,
                fare=fare
            )
            return redirect("chome")
    return render(request, "book_rides.html")
 
@login_required
def customer_rides(request):

    rides = Ride.objects.filter(
        customer=request.user
    )

    return render(
        request,
        "my_ride.html",
        {
            "rides": rides
        }
    )

@login_required
def available_rides(request):

    rides = Ride.objects.filter(
        driver=request.user,
        status="REQUESTED"
    )

    return render(
        request,
        "available_rides.html",
        {"rides": rides}
    )

@login_required
def accept_ride(request,ride_id):
    ride=Ride.objects.get(id=ride_id)
    ride.driver=request.user
    ride.status="ACCEPTED"
    ride.save()
    return redirect("driver_rides")

@login_required
def driver_ride(request):
    ride=Ride.objects.fiter(
        driver=request.user
    )
    return render(request,"driver_riders.html",{"ride":ride})

@login_required
def update_status(request,ride_id,status):
    ride=Ride.objects.get(id=ride_id)
    ride.status=status
    ride.save()
    return redirect("driver_rides")


@login_required
def accept_ride(request, ride_id):

    ride = get_object_or_404(
        Ride,
        id=ride_id,
        driver=request.user
    )

    if ride.status == "REQUESTED":
        ride.status = "ACCEPTED"
        ride.save()

    return redirect("available_rides")

@login_required
def cancel_ride(request, ride_id):

    ride = get_object_or_404(
        Ride,
        id=ride_id,
        driver=request.user
    )

    if ride.status == "REQUESTED":
        ride.status = "CANCELLED"
        ride.save()

    return redirect("available_rides")
