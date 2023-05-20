import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.validators import RegexValidator

from AdSpot.models import AdStatus, AdType, Advertisement


class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=254, help_text='Adres email jest wymagany do rejestracji')
	
	class Meta:
		model = User
		fields = ('username', 'email', 'password1', 'password2', )

	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		try:
			account = User.objects.get(email=email)
		except User.DoesNotExist:
			return email
		raise forms.ValidationError('Email "%s" jest już w użyciu.' % account.email)

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			account = User.objects.get(username=username)
		except User.DoesNotExist:
			return username
		raise forms.ValidationError('Nazwa użytkownika "%s" jest już w użyciu.' % account.username)

class LoginForm(forms.Form):
	username = forms.CharField(max_length=254, help_text='Nazwa użytkownika jest wymagana do zalogowania.')
	password = forms.CharField(widget=forms.PasswordInput, help_text="Hasło jest wymagane do zalogowania.")

	class Meta:
		model = User
		fields = ('username', 'password')

	def check(self, request):
		username = self.cleaned_data['username']
		password = self.cleaned_data['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return True
		self.add_error(None, "Nieprawidłowe dane logowania")
		return False
	
class DeleteAccountForm(forms.Form):
	password = forms.CharField(widget=forms.PasswordInput, help_text="Hasło jest wymagane.")

	class Meta:
		model = User
		fields = ('password')

	def check(self, request, username):
		password = self.cleaned_data['password']
		user = authenticate(request, username=username, password=password)
		if user is not None:
			return True
		self.add_error(None, "Nieprawidłowe hasło")
		return False
	
class CustomPasswordChangeForm(forms.Form):
    
	old_password = forms.CharField(
        strip=True,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text='Wprowadź obecne hasło',
    )  
    
	new_password = forms.CharField(
        strip=True,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text='Wprowadź nowe hasło'
    )    
    
	new_password_confirmation = forms.CharField(
        strip=True,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        help_text='Wprowadź to samo hasło jak wcześniej, dla weryfikacji.'
    )

	class Meta:
		model = User
		fields = ('old_password', 'new_password', 'new_password_confirmation')

class AddAdvertForm(forms.Form):  
	name = forms.CharField(
        strip=True,
        help_text='Podaj tytuł ogłoszenia',
		max_length=100
    )  
    
	description = forms.CharField(strip=True, help_text='Podaj opis ogłoszenia')

	localization = forms.CharField(
        strip=True,
        help_text='Podaj lokalizację',
		max_length=100
    )  	
    
	contact_number = forms.CharField(
        strip=True,
		max_length=12,
        help_text='Podaj numer kontaktowy',
        validators=[
            RegexValidator(
                regex=r'^\d{3}\s\d{3}\s\d{3}$',
                message='Wprowadź numer w formacie "xxx xxx xxx"'
            )
        ],	
    )

	image = forms.ImageField() 

	def create_advert(self, user, adType):
		name = self.cleaned_data['name']
		description = self.cleaned_data['description']
		contact_number = self.cleaned_data['contact_number']
		localization = self.cleaned_data['localization']
		image = self.cleaned_data['image']

		return Advertisement(name = name, description = description, 
		       date = datetime.datetime.now(), status = AdStatus[0],
		       contact_number = contact_number, localization = localization,
			   user = user, adType = adType, image = image)	    		    