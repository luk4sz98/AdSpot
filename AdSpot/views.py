from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import logout

from AdSpot.models import AdType, Advertisement

def index(request):
    data = __getAdverts()
    return render(request, 'index.html', data)

def advertisement(request, id):
    advertisement = Advertisement.objects.get(pk=id)
    data = {'advertisement' : advertisement}
    return render(request, 'advertisement.html', data)

def login(request):
    return render(request, 'registration/login.html')

def logout_view(request):
    logout(request)
    data = __getAdverts()
    return render(request, 'index.html', data)

def registration_view(request):
    return render(request, 'registration/registration.html')

def __getAdverts():
    advertisements = Advertisement.objects.all()
    data = {'advertisements' : advertisements}
    return data