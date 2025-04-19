import random
from .models import Regle, Individu

def food_consumption(age):
    regle = Regle.objects.first()
    if age == 1:
        return regle.food_consumption_age_1
    elif age == 2:
        return regle.food_consumption_age_2
    elif age >= 3:
        return regle.food_consumption_age_3_or_more
    return 0

def update_food(elevage):
    individus = elevage.individus.filter(state__in=['present', 'pregnant']).order_by('sex')
    regle = Regle.objects.first()
    for individu in individus:
        food_needed = food_consumption(individu.age)*30
        if elevage.foodLevel >= food_needed:
            elevage.foodLevel -= food_needed
            individu.age += 1
            individu.save()
        else:
            individu.state = 'dead'
            individu.save()

def sell_rabbits(elevage, male_rabbits_to_sell, female_rabbits_to_sell):
    male_rabbits = elevage.individus.filter(sex='M', state__in=['present', 'pregnant'])[:male_rabbits_to_sell]
    for rabbit in male_rabbits:
        rabbit.state = 'sold'
        rabbit.save()

    female_rabbits = elevage.individus.filter(sex='F', state__in=['present', 'pregnant'])[:female_rabbits_to_sell]
    for rabbit in female_rabbits:
        rabbit.state = 'sold'
        rabbit.save()

    elevage.male_rabbits -= male_rabbits_to_sell
    elevage.female_rabbits -= female_rabbits_to_sell
    regle = Regle.objects.first()
    elevage.money += (male_rabbits_to_sell + female_rabbits_to_sell) * regle.rabbit_sale_price

def buy_resources(elevage, food_to_buy, cages_to_buy):
    regle = Regle.objects.first()
    elevage.foodLevel += food_to_buy*1000
    elevage.cageNumber += cages_to_buy
    elevage.money -= (food_to_buy * regle.food_price + cages_to_buy * regle.cage_price)

def process_actions(elevage, male_rabbits_to_sell, female_rabbits_to_sell, food_to_buy, cages_to_buy):
    sell_rabbits(elevage, male_rabbits_to_sell, female_rabbits_to_sell)
    buy_resources(elevage, food_to_buy, cages_to_buy)
    elevage.save()

def can_reproduce(individu):
    regle = Regle.objects.first()
    return (
        individu.sex == 'F' and
        regle.reproduction_start_age <= individu.age <= regle.reproduction_end_age and
        individu.state == 'present'
    )

def reproduce(elevage):
    regle = Regle.objects.first()
    females = list(elevage.individus.filter(
        sex='F',
        state='present',
        age__gte=regle.reproduction_start_age,
        age__lte=regle.reproduction_end_age
    ))
    if females:
        num_to_impregnate = random.randint(1, len(females))
        selected_females = random.sample(females, num_to_impregnate)
        for female in selected_females:
            litter_size = random.randint(1, regle.litter_size)
            for _ in range(litter_size):
                Individu.objects.create(
                    elevage=elevage,
                    sex=random.choice(['M', 'F']),
                    age=1,
                    state='present'
                )
            female.state = 'pregnant'
            female.pregnancy_start_month = elevage.month
            female.save()

def update_pregnancy(elevage):
    regle = Regle.objects.first()
    pregnant_females = elevage.individus.filter(sex='F', state='pregnant')
    for female in pregnant_females:
        if elevage.month - female.pregnancy_start_month >= regle.gestation_duration:
            female.state = 'present'
            female.pregnancy_start_month = None
        female.save()

def handle_overpopulation(elevage):
    regle = Regle.objects.first()
    adults = elevage.individus.filter(age__gte=2, state__in=['present', 'pregnant']).count()
    cages_available = elevage.cageNumber
    overpopulation_threshold = cages_available * regle.overpopulation_threshold

    if adults > overpopulation_threshold:
        surplus = adults - overpopulation_threshold
        num_to_die = random.randint(surplus, adults)  
        sick_individus = list(elevage.individus.filter(age__gte=1, state__in=['present', 'pregnant']))
        selected_to_die = random.sample(sick_individus, num_to_die)  
        for individu in selected_to_die:
            individu.state = 'dead'
            individu.save()

def update_rabbit_counts(elevage):
    elevage.male_rabbits = elevage.individus.filter(sex='M', state__in=['present', 'pregnant']).count()
    elevage.female_rabbits = elevage.individus.filter(sex='F', state__in=['present', 'pregnant']).count()
    elevage.save()

def update(elevage):
    update_food(elevage)
    update_pregnancy(elevage)
    reproduce(elevage)
    handle_overpopulation(elevage)
    update_rabbit_counts(elevage)  # Aggiorna i conteggi dei conigli
    elevage.month += 1
    elevage.save()