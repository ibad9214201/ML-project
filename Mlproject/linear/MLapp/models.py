from django.db import models

# Create your models here.
from django.db import models

class HousePrice(models.Model):
    Size_sqft = models.IntegerField()
    Bedrooms = models.IntegerField()
    Bathrooms = models.IntegerField()
    Age_years = models.IntegerField()
    Distance_to_city_km = models.FloatField()
    Location_type = models.CharField(max_length=30)
    Condition = models.CharField(max_length=20)
    House_Price = models.FloatField()
    def __str__(self):
        return f"{self.Size_sqft} sqft - {self.House_Price}"

from django.db import models

class FootballMatch(models.Model):
# Fields
    Weather = models.CharField(max_length=20,)
    Temperature = models.CharField(max_length=10, help_text="Temperature: Hot, Mild, Cool")
    Humidity = models.CharField(max_length=10,)
    Wind = models.CharField(max_length=10,)
    Weekend = models.CharField(max_length=20)
    Ground_Condition = models.CharField(max_length=20,)
    Play_Football = models.CharField(max_length=20,help_text="True if football is played (Yes), False if not (No)")

    def __str__(self):
        play_status = "Play" if self.Play_Football else "No Play"
        return f"{self.Weather.capitalize()} - {play_status}"