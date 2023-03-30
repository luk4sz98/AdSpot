from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


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
	