import datetime
from django.shortcuts import redirect, render
from django.contrib.auth import logout, update_session_auth_hash
from AdSpot.forms import AddAdvertForm, DeleteAccountForm, LoginForm, RegistrationForm, CustomPasswordChangeForm
from django.contrib.auth.models import User
from django.contrib import messages

from AdSpot.models import AdStatus, AdType, Advertisement

def index(request):
    data = __getAdverts()
    return render(request, 'index.html', data)

def advertisement(request, id):
    advertisement = Advertisement.objects.get(pk=id)

    data = {'advertisement' : advertisement, 'user' : advertisement.user}
    return render(request, 'advertisement.html', data)

def add_advertisement_view(request):
    if not request.user.is_authenticated:
        messages.warning(request, f"Musisz się zalogować by uzyskać dostęp!")
        return redirect("/")
    
    context = {}
    if request.method == "POST":
        add_advert_form = AddAdvertForm(request.POST)
        if add_advert_form.is_valid():
            adTypeName = request.POST.get('adType')
            adType = AdType.objects.get(name = adTypeName)
            new_advert = add_advert_form.create_advert(request.user, adType)
            if new_advert is not None:
                new_advert.save()
                messages.info(request, f'Ogłoszenie zostało dodane. Musi zostać zaakceptowane przez moderatora :)')
                advertisements = Advertisement.objects.filter(user_id = request.user)
                data = {'advertisements': advertisements}
                return render(request, 'userPendingAdverts.html', data)
        add_advert_form.add_error(None, "Nieprawidłowe dane")  
    else:
        add_advert_form = AddAdvertForm()

    context = {'add_advert_form': add_advert_form, 'adTypes': AdType.objects.all()}   
    return render(request, 'addAdvertisement.html', context)

def getMyAdvertisements(request):
    if not request.user.is_authenticated:
        messages.warning(request, f"Musisz się zalogować by uzyskać dostęp!")
        return redirect("/") 
    advertisements = Advertisement.objects.filter(user_id = request.user)
    advertisements = advertisements.filter(status__icontains = 'accepted')
    data = {'advertisements': advertisements, "areMine": "true"}
    return render(request, 'userActiveAdverts.html', data)

def user_pending_adverts_view(request):
    if not request.user.is_authenticated:
        messages.warning(request, f"Musisz się zalogować by uzyskać dostęp!")
        return redirect("/") 
    advertisements = Advertisement.objects.filter(user_id = request.user)
    advertisements = advertisements.filter(status__icontains = 'pending')
    data = {'advertisements': advertisements}
    return render(request, 'userPendingAdverts.html', data)

def deleteAdvertisement(request, id):
    if not request.user.is_authenticated:
        messages.warning(request, f"Musisz się zalogować by uzyskać dostęp!")
        return redirect("/")    
    
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

def user_settings(request):
    user = request.user
    if not user.is_authenticated:
        messages.warning(request, f"Musisz się zalogować by uzyskać dostęp!")
        return redirect("/")
    
    context = {}
    context = {'delete_account_form': DeleteAccountForm()}

    return render(request, 'user_settings/settings.html', context)

def delete_account(request):
    user = request.user
    if not user.is_authenticated:
        messages.warning(request, f"Musisz się zalogować by uzyskać dostęp!")
        return redirect("/")
    if request.method == 'POST':
        user_from_db = User.objects.get(pk=user.pk)
        form = DeleteAccountForm(request.POST)
        if form.is_valid() and form.check(request, user_from_db.username):
            logout(request)
            user_from_db.delete()
            messages.success(request, f"Twoje konto zostało usunięte.")
            return redirect('/')   
        context = {'delete_account_form': form}        
        return render(request, 'user_settings/settings.html', context)
    
    messages.error(request, 'Nieprawidłowe żądanie!')
    return redirect(request, '/')   

def change_password(request):
    user = request.user     
    if not user.is_authenticated:
        messages.warning(request, f"Musisz się zalogować by uzyskać dostęp!")
        return redirect("/")
    if request.method == 'POST':
        context = {}
        user_from_db = User.objects.get(pk=user.pk)
        form = CustomPasswordChangeForm(request.POST)
        if form.is_valid():
            current_password = form.cleaned_data['old_password']
            new_password = form.cleaned_data['new_password']
            new_password_confirmation = form.cleaned_data['new_password_confirmation']
            if (not user_from_db.check_password(current_password) or
                new_password != new_password_confirmation):
                form.add_error(None, "Nieprawidłowe hasła, spróbuj jeszcze raz.")
                context = {'change_password_form': form}
                return render(request, 'user_settings/settings.html', context)

            user_from_db.set_password(new_password)
            user_from_db.save()
            update_session_auth_hash(request, user_from_db)
            messages.success(request, f"Twoje hasło zostało zmienione")
            return redirect('/') 
        form.add_error(None, "Nieprawidłowe dane, sprawdz podane hasła")  
        context = {'change_password_form': form}        
        return render(request, 'user_settings/settings.html', context)
    
    messages.error(request, 'Nieprawidłowe żądanie!')
    return redirect(request, '/')      

def __getAdverts():
    advertisements = Advertisement.objects.all()
    advertisements = advertisements.filter(status__icontains = 'accepted')
    data = {'advertisements' : advertisements}
    return data