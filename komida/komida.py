# Based on the API this site uses: https://app.growzer.be/komida-calendar
# e.g. https://app.growzer.be/MenuPlanner/GetMenuPlanner?locationId=9038&stringDate=2023-01-11&customerId=7622
import requests as requests

KOMIDA_CUSTOMER_ID = 7622
locations = {"CST": 8198, "CMI": 8199, "CGB": 8200, "CDE": 8201, "HZS": 8202, "ONLINE": 9038}


def menu_item_to_string(menu_item):
    return f"{menu_item['MenuName']} ({menu_item['TakeawayPriceGross']}/{menu_item['DeliveryPriceGross']}€)"


def get_menu(location, date):
    assert location in locations

    location_id = locations[location]

    # put date in yyy-mm-dd format
    date = date.strftime("%Y-%m-%d")

    # get the menu
    url = f"https://app.growzer.be/MenuPlanner/GetMenuPlanner?locationId={location_id}&stringDate={date}&customerId={KOMIDA_CUSTOMER_ID}"
    response = requests.get(url)
    menu = response.json()
    assert menu["success"]

    # get the menu items
    menu_items = menu["data"]["menuPlannerList"]
    text = "\n".join([f"- {menu_item_to_string(item)}" for item in menu_items])

    return text
