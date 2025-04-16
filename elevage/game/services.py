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

def sell_rabbits(elevage, male_rabbits_to_sell, female_rabbits_to_sell):
    male_rabbits = elevage.individus.filter(sex='M', state='present')[:male_rabbits_to_sell]
    for rabbit in male_rabbits:
        rabbit.state = 'sold'
        rabbit.save()

    female_rabbits = elevage.individus.filter(sex='F', state='present')[:female_rabbits_to_sell]
    for rabbit in female_rabbits:
        rabbit.state = 'sold'
        rabbit.save()

    elevage.male_rabbits -= male_rabbits_to_sell
    elevage.female_rabbits -= female_rabbits_to_sell
    regle = Regle.objects.first()
    elevage.money += (male_rabbits_to_sell + female_rabbits_to_sell) * regle.rabbit_sale_price

def buy_resources(elevage, food_to_buy, cages_to_buy):
    regle = Regle.objects.first()
    elevage.foodLevel += food_to_buy
    elevage.cageNumber += cages_to_buy
    elevage.money -= (food_to_buy * regle.food_price + cages_to_buy * regle.cage_price)

def process_actions(elevage, male_rabbits_to_sell, female_rabbits_to_sell, food_to_buy, cages_to_buy):
    sell_rabbits(elevage, male_rabbits_to_sell, female_rabbits_to_sell)
    buy_resources(elevage, food_to_buy, cages_to_buy)
    elevage.save()