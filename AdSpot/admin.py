from django.contrib import admin

from AdSpot.models import AdType, Advertisement

admin.site.register(AdType)
admin.site.register(Advertisement)
#tutaj wypisujemy to co admin będzie widział w swoim panelu 