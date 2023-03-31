from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


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