from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from AdSpot.views import addAdvertisementView, advertisement, index, addAdvertisement
# routing 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('ad/<id>/', advertisement, name='advertisement'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('add/', addAdvertisementView, name='addAdvertisementView'),
    path('add/', addAdvertisement, name='addAdvertisement')
]
