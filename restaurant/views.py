from django.shortcuts import render
import random
from datetime import datetime, timedelta

special_dishes = {
    "pit_lane_panna_cotta": ["Pit Lane Panna Cotta $8", " – Smooth and perfectly timed, just like a well-executed pit stop."],
    "chicane_chocolate_mousse": ["Chicane Chocolate Mousse $9", " – Rich and smooth, twisting its way to the finish."], 
    "strategy_strudel": ["Strategy Strudel $10", "– A dessert that’s as complex and satisfying as a winning race strategy."]
}

def show_main(request):
    """ renders main.html with general info about the restaurant """

    # rednering the main.html template
    return render(request, 'restaurant/main.html')

def make_order(request):
    """ renders show_all.html with all quotes and images """

    special_dish, special_description = random.choice(list(special_dishes.items()))
    context = {
            'special_dish': special_dish,
            'special_name': special_description[0],
            'special_description': special_description[1]
        }

    # rednering the main.html template
    return render(request, 'restaurant/order.html', context)

def submit(request):
    """" handles form submission """

    template_name = 'restaurant/confirmation.html'

    if request.POST:
        ordered_items = []
        menu_items = {
            'leclerc_lasagna': "Leclerc's Lasagna",
            'pit_stop_pesto_penne': "Pit Stop Pesto Penne",
            'sainz_scuderia_spaghetti': "Sainz’s Scuderia Spaghetti",
            'fuel_strategy_fettuccine': "Fuel Strategy Fettuccine",
            'pole_position_pappardelle': "Pole Position Pappardelle",
            'binotto_bolognese_blunder': "Binotto’s Bolognese Blunder",
            'pit_crew_pepperoni': "Pit Crew Pepperoni",
            'extra_cheese': "Extra Cheese",
            'mushrooms': "Mushrooms",
            'black_olives': "Black Olives",
            'green_peppers': "Green Peppers",
            'extra_pepperoni': "Extra Pepperoni",
            'onions': "Onions",
            'pit_lane_panna_cotta': "Pit Lane Panna Cotta",
            'chicane_chocolate_mousse': "Chicane Chocolate Mousse",
            'strategy_strudel': "Strategy Strudel",
            'daily_special': "Today's Special"
        }

        # iterating over the POST data and identify which items were ordered
        for key, _ in request.POST.items():
            if key in menu_items:
                ordered_items.append(menu_items[key])

        # getting customer information
        customer_name = request.POST.get('customer_name')
        customer_phone = request.POST.get('customer_phone')
        customer_email = request.POST.get('customer_email')
        special_instructions = request.POST.get('special_instructions', '')

        # calculating the expected order completion time (randomly between 30 and 60 minutes)
        preparation_time = random.randint(30, 60) - 240
        expected_ready_time = datetime.now() + timedelta(minutes = preparation_time)
        formatted_ready_time = expected_ready_time.strftime('%I:%M %p')

        # preparing context data for the confirmation page
        context = {
            'ordered_items': ordered_items,
            'customer_name': customer_name,
            'customer_phone': customer_phone,
            'customer_email': customer_email,
            'special_instructions': special_instructions,
            'ready_time': formatted_ready_time
        }
        return render(request, template_name, context)

    return render(request, template_name)