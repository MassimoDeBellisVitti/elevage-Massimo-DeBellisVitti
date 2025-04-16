from .models import Regle

def update_food_and_advance_month(elevage):
    individus = elevage.individus.filter(state='present').order_by('sex')
    regle = Regle.objects.first()
    elevage.month += 1
    for individu in individus:
        food_needed = regle.food_consumption(individu.age)
        if elevage.foodLevel >= food_needed:
            elevage.foodLevel -= food_needed
            individu.age += 1
            individu.save()
        else:
            individu.state = 'dead'
            individu.save()
    elevage.save()