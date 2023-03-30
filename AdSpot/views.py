from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import logout, login
from AdSpot.forms import RegistrationForm
from django.contrib.auth.models import User
from django.contrib import messages

from AdSpot.models import AdType, Advertisement

def index(request):
    data = __getAdverts()
    return render(request, 'index.html', data)

def advertisement(request, id):
    advertisement = Advertisement.objects.get(pk=id)
    data = {'advertisement' : advertisement}
    return render(request, 'advertisement.html', data)

def login_view(request):
    return render(request, 'authorizathion/login.html')

def logout_view(request):
    logout(request)
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
    return render(request, 'authorizathion/registration.html', context)

def __getAdverts():
    advertisements = Advertisement.objects.all()
    data = {'advertisements' : advertisements}
    return data