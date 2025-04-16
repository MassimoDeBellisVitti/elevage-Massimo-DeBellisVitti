from .models import Regle

def food_consumption(age):
    regle = Regle.objects.first()
    if age == 1:
        return regle.food_consumption_age_1
    elif age == 2:
        return regle.food_consumption_age_2
    elif age >= 3:
        return regle.food_consumption_age_3_or_more
    return 0

def update_food_and_advance_month(elevage):
    individus = elevage.individus.filter(state='present').order_by('sex')
    elevage.month += 1
    for individu in individus:
        food_needed = food_consumption(individu.age)
        if elevage.foodLevel >= food_needed:
            elevage.foodLevel -= food_needed
            individu.age += 1
            individu.save()
        else:
            individu.state = 'dead'
            individu.save()
    elevage.save()