# elevage-Massimo-DeBellisVitti
🐰 Rabbit Farm Management Game

Rabbit Farm Management is a turn-based strategy simulation where players manage a rabbit farm, optimizing limited resources through careful planning and smart decisions.

🎯 Game Objective

Manage your farm by:
	•	Breeding rabbits (males and females)
	•	Feeding them
	•	Expanding cages
	•	Selling adult rabbits
	•	Managing money wisely

The goal is to grow your farm sustainably while balancing available resources.

🚀 Game Start
	•	Players select the initial quantities of:
	•	Rabbits (males and females)
	•	Food
	•	Cages
	•	Money
	•	The game begins with these starting resources.

🔁 Turn Structure
	•	Each turn represents one month.
	•	During a turn, players can:
	•	Buy food (1 unit = 1 kg)
	•	Sell adult rabbits (3 months or older)
	•	Buy additional cages
	•	After each turn, the farm state updates automatically (reproduction, feeding, deaths, etc.).

🐇 Reproduction Rules
	•	Females reach maturity at 6 months and can reproduce until 4 years.
	•	Gestation lasts 1 month.
	•	Each litter produces 1 to 4 kits (baby rabbits).
	•	Females can become pregnant again a few days after giving birth.
	•	Important: Reproduction only occurs if there is at least one male rabbit aged 3 months or older in the farm.

📈 Growth and Maturity
	•	Rabbits are considered adults at 3 months old.
	•	Only adults (3+ months) can be sold.
	•	When selling, older rabbits are sold first.

🥕 Feeding Rules
	•	Food Consumption:
	•	1st month: 0 kg (milk from the mother)
	•	2nd month: 3 kg/month (100 g/day)
	•	3rd month and older: 7.5 kg/month (250 g/day)
	•	Consequence: Rabbits that are not fed for a full month will die.

🏠 Cage Rules
	•	Each cage can safely hold up to 6 rabbits.
	•	Overpopulation (10 rabbits or more per cage) increases the risk of disease and death.
	•	Kits under 1 month old do not count towards overpopulation limits.

📜 License

This project is for educational and simulation purposes.