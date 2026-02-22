MENU = {
    "tea": {
        "ingredients": {
            "water": 50,
            "milk": 10,
            "sugar": 20,
        },
        "cost": 20,
    },
    "coffee": {
        "ingredients": {
            "water": 50,
            "milk": 10,
            "coffee": 12,
            "sugar": 20,
        },
        "cost": 40,
    },
    "espresso": {
        "ingredients": {
            "water": 50,
            "coffee": 18,
            "sugar": 25,
        },
        "cost": 100,
    },
    "latte": {
        "ingredients": {
            "water": 200,
            "milk": 150,
            "coffee": 24,
            "sugar": 50,
        },
        "cost": 120,
    },
    "cappuccino": {
        "ingredients": {
            "water": 250,
            "milk": 100,
            "coffee": 24,
            "sugar": 50,
        },
        "cost": 150,
    }
}

total_amount = 0
available_resources = {
    "water": 2000,
    "milk": 1000,
    "coffee": 200,
    "sugar": 400,
}

is_on = True


def is_resource_sufficient(order_ingredients):
    is_enough = True
    for item in order_ingredients:
        if order_ingredients[item] > available_resources[item]:
            print(f"sorry there is not enough {item}.")
            is_enough = False
    return is_enough

while is_on:
    choice = input("what would you like? (tea/coffee/espresso/latte/cappuccino) || buttons? (off/report): ").lower().strip()

    while choice not in MENU and choice not in ["off", "report"]:
        print("Incorrect input, please try again!")
        choice = input("What would you like? (tea/coffee/espresso/latte/cappuccino) || buttons? (off/report): ").lower().strip()
    
    if choice == "off":
        is_on = False
        print("Coffee Machine is turned off !")

    elif choice == "report":
        # print(available_resources.items())
        print("Available Resources:")
        for item, amount in available_resources.items():
            print(f"{item}: {amount}")
        
    elif choice in MENU:
        drink = MENU[choice]
        print(drink)
        if is_resource_sufficient(drink["ingredients"]):
            payment = drink["cost"]
            print(f"Cost of {choice}:", "$", payment)
            
            for item in drink["ingredients"]:
                available_resources[item] -= drink["ingredients"][item]

            print("Here is your drink. Enjoy!")
            total_amount += payment
            print("Total collection of the day:", "$", total_amount)
            
        else:
            print("Not enough available_resources to make your drink.")
            print(available_resources)
    
