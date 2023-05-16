from django.db import models
from django.contrib.auth.models import User

class AdType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

AdStatus = (('pending', 'Waiting for'),
            ('accepted', 'Accepted'),
            ('rejected', 'Rejected'))

class Advertisement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date = models.DateField()
    contact_number = models.CharField(max_length=12, default="123 456 789")
    localization = models.CharField(max_length=100)
    adType = models.ForeignKey(AdType, on_delete=models.CASCADE, null=False)
    status = models.CharField(choices=AdStatus, max_length=30, default=AdStatus[0])
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

