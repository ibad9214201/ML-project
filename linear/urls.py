"""
URL configuration for linear project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from numpy import poly

from MLapp.views import Decisiontree, Decisiontree_load_data, Edit_Data, GradientBoosting, House_price, delete_employee, mainhtml, poly_nomial, poly_predict, predictvalue, update_Data

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('excel/',House,name="House"),
    path('mainhtml/',mainhtml,name="mainhtml"),
    path('Houseprice/',House_price,name="Houseprice"),
    path('predictvalue/',predictvalue,name="predictvalue"),
    path('delete_employee/',delete_employee,name="delete_employee"),
    path('Edit_Data/',Edit_Data,name="Edit_Data"),
    path('update_Data/',update_Data,name="update_Data"),
    #Polynomial regression 
    path('poly_nomial/',poly_nomial,name="poly_nomial"),
    path('poly_predict/',poly_predict,name="poly_predict"),
    #Decisiontree
    path('Decisiontree_load_data/',Decisiontree_load_data,name="Decisiontree_load_data"),
    path('Decisiontree/',Decisiontree,name="Decisiontree"),
    path('GradientBoosting/',GradientBoosting,name="GradientBoosting"),



    
]
