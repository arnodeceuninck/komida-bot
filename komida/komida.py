# Based on the API this site uses: https://app.growzer.be/komida-calendar
# e.g. https://app.growzer.be/MenuPlanner/GetMenuPlanner?locationId=9038&stringDate=2023-01-11&customerId=7622
import requests as requests

KOMIDA_CUSTOMER_ID = 7622
locations = {"CST": (8198, "Stadscampus"), "CMI": (8199, "Campus Middelheim"), "CGB": (8200, "Campus Groenenborger"),
             "CDE": (8201, "Campus Drie Eiken"), "HZS": (8202, "Hogere Zeevaartschool"),
             "ONLINE": (9038, "Komida Online")}
icons = {"concept salade": "🥗", "broodje in de kijker": "🥖", "maaltijden om op te warmen": "🔥", "soep": "🍵",
         "conceptsalades": "🥗", "daily food": "🍝", "streetfood": "🍔"}


def menu_item_to_string(menu_item):
    section = menu_item["SectionName"].strip().lower() # Strip because there are some trailing spaces
    if section in icons:
        icon = icons[section]
    else:
        icon = "😋"
    return f"{icon} {menu_item['MenuName']} (€{menu_item['TakeawayPriceGross']:.2f} / €{menu_item['DeliveryPriceGross']:.2f})"


def get_menu(location, date):
    assert location.upper() in locations

    location_id = locations[location][0]
    location_name = locations[location][1]

    # put date in yyy-mm-dd format
    date_str = date.strftime("%Y-%m-%d")

    # get the menu
    url = f"https://app.growzer.be/MenuPlanner/GetMenuPlanner?locationId={location_id}&stringDate={date_str}&customerId={KOMIDA_CUSTOMER_ID}"
    print(url)
    response = requests.get(url)
    menu = response.json()
    assert menu["success"]

    # get the menu items
    menu_items = menu["data"]["menuPlannerList"]
    text = "\n".join([f"{menu_item_to_string(item)}" for item in menu_items])

    datetext = date.strftime("%A %d %B")
    full_text = f"Menu from {datetext} in {location_name}:\n\n{text}"

    return full_text
