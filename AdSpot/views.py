import datetime
from django.http import HttpResponse
from django.shortcuts import render

from AdSpot.models import AdStatus, AdType, Advertisement

def index(request):
    advertisements = Advertisement.objects.all() # select * from Advertisement
    one = AdType.objects.get(pk=2) # select * from AdType where id=2
    filter = Advertisement.objects.filter(adType = 1) # select * from Advertisement where adType=1
    null = Advertisement.objects.filter(description__isnull=False) # select * from Advertisement where description != null
    contains = Advertisement.objects.filter(name__icontains='cos')
    data = {'advertisements' : advertisements}
    return render(request, 'index.html', data)

def advertisement(request, id):
    advertisement = Advertisement.objects.get(pk=id)
    data = {'advertisement' : advertisement}
    return render(request, 'advertisement.html', data)

def addAdvertisementView(request):
    adTypes = AdType.objects.all()
    data = {'adTypes': adTypes}
    return render(request, 'addAdvertisement.html', data)


def addAdvertisement(request):
    name = request.POST.get('name')
    description = request.POST.get('description')
    user = request.user
    adTypeName = request.POST.get('adType')
    adType = AdType.objects.get(name = adTypeName)
    date = datetime.datetime.now()
    status = AdStatus[0]
    data = Advertisement(name = name, description = description,  date = date, status= status, user = user, adType = adType)
    data.save()
    return render(request, 'added.html')

def getMyAdvertisements(request): 
    advertisements = Advertisement.objects.filter(user_id = request.user)
    data = {'advertisements': advertisements}
    return render(request, 'index.html',data)