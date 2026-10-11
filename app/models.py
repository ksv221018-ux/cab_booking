from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    ROLE_CHOICE=(
        ("CUSTOMER","Customer"),
        ("Driver","DRIVER")
    )
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    role=models.CharField(max_length=200,choices=ROLE_CHOICE)

class Route(models.Model):
    source = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    distance = models.IntegerField()
    def __str__(self):
        return f"{self.source} to {self.destination}"

class Ride(models.Model):
    STATUS_CHOICE=(
        ("REQUESTED","Requested"),
        ("ACCEPTED","Accepted"),
        ("STARTED","Started"),
        ("Completed","COMPLETED"),
        ("CANCLED","Cancled")
    )

    customer=models.ForeignKey(
        User,on_delete=models.CASCADE,
        related_name="customer_ride"
    )
    driver=models.ForeignKey(
        User,on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="driver_ride"
    )
    route = models.ForeignKey(
        Route,
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )

    distance = models.IntegerField(
        null=True,
        blank=True
    )
    driver = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="driver_rides"
    )
    pickup_location=models.CharField(max_length=200)
    drop_location=models.CharField(max_length=200)
    fare=models.IntegerField()
    status=models.CharField(max_length=200,choices=STATUS_CHOICE,default='REQUESTED')
    created_at=models.DateTimeField(auto_now_add=True)
