import datetime
from django.shortcuts import redirect, render
from django.contrib.auth import logout
from AdSpot.forms import LoginForm, RegistrationForm
from django.contrib.auth.models import User
from django.contrib import messages

from AdSpot.models import AdStatus, AdType, Advertisement

def index(request):
    data = __getAdverts()
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
    advertisements = advertisements.filter(status__icontains = 'accepted')
    data = {'advertisements': advertisements, "areMine": "true"}
    return render(request, 'index.html',data)


def deleteAdvertisement(request, id):
    advertisement = Advertisement.objects.get(pk=id)

    advertisement.delete()
    messages.success(request, f'Usunięto.')

    return redirect("myAdvertisements")


def login_view(request):
    user = request.user

    if user.is_authenticated:
        messages.warning(request, f"Jesteś już zalogowany")
        return redirect("/")
    context = {}   

    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            userExist = form.check(request)
            if userExist:
                messages.success(request, f'Zalogowałeś się.')
                return redirect("/")
    else:
        form = LoginForm()
        
    context = {'login_form': form}

    return render(request, 'authorization/login.html', context)

def logout_view(request):
    logout(request)
    user = request.user
    if not user.is_authenticated:
        messages.success(request, f'Wylogowałeś się.')
    data = __getAdverts()
    return render(request, 'index.html', data)

def registration_view(request):
    user = request.user
    if user.is_authenticated:
        messages.warning(request, f"Jesteś już zarejestrowany!")
        return redirect("/")
    context = {}

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email').lower()
            user = User.objects.get(email=email)
            messages.success(request, f'Konto {user.username} zostało utworzone. Możesz się teraz zalogować.')
            return redirect("login/")
        else:
            context['registration_form'] = form

    return render(request, 'authorization/registration.html', context)

def __getAdverts():
    advertisements = Advertisement.objects.all()
    advertisements = advertisements.filter(status__icontains = 'accepted')
    data = {'advertisements' : advertisements}
    return data