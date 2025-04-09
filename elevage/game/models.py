from django.db import models

class Elevage(models.Model):
    
    name = models.CharField(max_length=100)
    male_rabbits = models.IntegerField()
    female_rabbits = models.IntegerField()
    foodLevel = models.IntegerField()
    cageNumber = models.IntegerField()
    money = models.IntegerField()
    month = models.IntegerField(default=0)
    

    def __str__(self):
        return self.name

# Create your models here.
