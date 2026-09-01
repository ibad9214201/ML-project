from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import FootballMatch, Footballclassification, HousePrice
class House_admin(admin.ModelAdmin):
    list_display=[
        "id","Size_sqft",'Bedrooms','Bathrooms','Age_years','Distance_to_city_km','Location_type','Condition','House_Price'
    ]

admin.site.register(HousePrice,House_admin)
class FootballMatchAdmin(admin.ModelAdmin):
    list_display = ('Weather', 'Temperature', 'Humidity', 'Wind', 'Weekend', 'Ground_Condition', 'Play_Football')

admin.site.register(FootballMatch, FootballMatchAdmin)
class FootballclassAdmin(admin.ModelAdmin):
    list_display = ('Weather', 'Temperature', 'Humidity', 'Wind', 'Weekend', 'Ground_Condition','Time_of_Day', 'Play_Football')

admin.site.register(Footballclassification, FootballclassAdmin)

