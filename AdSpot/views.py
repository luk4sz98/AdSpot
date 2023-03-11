from django.http import HttpResponse
from django.shortcuts import render

from AdSpot.models import AdType, Advertisement

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