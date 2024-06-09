from django.db import models


# Create your models here.

class ProfileImage(models.Model):
    image = models.CharField(default="NO IMAGE")

    def __str__(self):
        return self.image


class Car(models.Model):
    model = models.CharField(max_length=200)

    def __str__(self):
        return self.model


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    cars = models.ManyToManyField(Car)
    img = models.OneToOneField(ProfileImage, on_delete=models.CASCADE,null=True,blank=True)

    def __str__(self):
        return self.name


