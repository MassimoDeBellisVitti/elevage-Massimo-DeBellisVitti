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

class FemaleRabbit(models.Model):
    elevage = models.ForeignKey(Elevage, on_delete=models.CASCADE, related_name='females')
    age = models.IntegerField()
    pregnancyTime = models.IntegerField(default=0)

class MaleRabbit(models.Model):
    elevage = models.ForeignKey(Elevage, on_delete=models.CASCADE, related_name='males')
    age = models.IntegerField()