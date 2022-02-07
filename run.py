import time
from booking.booking import Booking


with Booking() as bot:
    bot.land_first_page()  # launch website to main page
    bot.change_currency(currency="EUR")  # change currency po EUR
    # Specify city of destination
    bot.select_place_to_go(input("Where you want to go? (input destination city)"))
    # Specify dates of desired check in and check out in YYYY-MM-DD format
    bot.select_dates(
        check_in_date=input("What is check-in date? (input in YYYY-MM-DD format)"),
        check_out_date=input("What is check-out date? (input in YYYY-MM-DD format)"),
    )
    # Specify quantity of travelling people from 1 up to 30
    bot.select_adults(int(input("How many people? (input number)")))
    bot.search_button()  # perform search
    bot.apply_filtration()  # apply filtration on search results
    bot.refresh()  # a workaround to let our bot to grab data properly
    bot.report_results()  # aggregating results to table
