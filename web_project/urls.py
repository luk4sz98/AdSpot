from django.contrib import admin
from django.urls import path

from AdSpot.views import advertisement, index
# routing 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('ad/<id>/', advertisement, name='advertisement')
]
