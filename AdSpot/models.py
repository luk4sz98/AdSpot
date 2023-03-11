from django.db import models

class AdType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Advertisement(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    date = models.DateField()
    adType = models.ForeignKey(AdType, on_delete=models.CASCADE, null=False)

    def __str__(self):
        return self.name


#enum
'''
IDEA_STATUS =(('pending', 'Waiting for')
('accepted', 'Accepted')
('done', 'Done'))

class Idea(models.Model) :
    status = models.charField(choices=IDEA_STATUS, max_length=30 default="pending")
    '''