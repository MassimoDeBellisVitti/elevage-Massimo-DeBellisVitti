from django.db import models

class Elevage(models.Model):
    
    name = models.CharField(max_length=100)
    male_rabbits = models.IntegerField()
    female_rabbits = models.IntegerField()
    foodLevel = models.IntegerField()
    cageNumber = models.IntegerField()
    money = models.IntegerField()
    month = models.IntegerField(default=1)
    

    def __str__(self):
        return self.name

# Create your models here.


class Individu(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    STATE_CHOICES = [
        ('present', 'Present'),
        ('sold', 'Sold'),
        ('dead', 'Dead'),
        ('pregnant', 'Pregnant'),
    ]

    elevage = models.ForeignKey(Elevage, on_delete=models.CASCADE, related_name='individus')
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    age = models.IntegerField()
    state = models.CharField(max_length=10, choices=STATE_CHOICES, default='present')
    pregnancy_start_month = models.IntegerField(null=True, blank=True)
    
class Regle(models.Model):
    food_price = models.IntegerField(default=5)
    cage_price = models.IntegerField(default=50)
    rabbit_sale_price = models.IntegerField(default=10)
    
    food_consumption_age_1 = models.IntegerField(default=0)
    food_consumption_age_2 = models.IntegerField(default=100)
    food_consumption_age_3_or_more = models.IntegerField(default=250)
    
    reproduction_start_age = models.IntegerField(default=6)
    reproduction_end_age = models.IntegerField(default=48)
    gestation_duration = models.IntegerField(default=1)
    litter_size = models.IntegerField(default=4)
    
    overpopulation_threshold = models.IntegerField(default=10)
    
    budget_limit = models.IntegerField(default=1000)
    male_rabbit_price = models.IntegerField(default=10)
    female_rabbit_price = models.IntegerField(default=10)






