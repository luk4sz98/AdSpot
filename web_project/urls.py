from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views

from AdSpot.views import *
# routing 
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index),
    path('ad/<id>/', advertisement, name='advertisement'),
    path('add/', add_advertisement_view, name='add_advertisement'),
    path('my', getMyAdvertisements, name='myAdvertisements' ),
    path('login/', login_view, name='login'),
    path('logout', logout_view),
    path('registration', registration_view),
    path('my/<id>', deleteAdvertisement, name='deleteAdvertisement'),
    path('settings', user_settings),
    path('delete_account', delete_account, name='delete_account'),
    path('change_password', change_password, name='change_password'),

    # resetowanie hasła
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='password_reset/password_reset_form.html',
        email_template_name='password_reset/password_reset_email.html',
        subject_template_name='password_reset/password_reset_subject.txt',
    ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset/password_reset_complete.html'), name='password_reset_complete'),    
]
