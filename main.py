# imports
from datetime import date, timedelta

import discord
from discord import app_commands

import komida

intents = discord.Intents.default()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)


# sync the slash command to your server
@client.event
async def on_ready():
    guilds = [guild for guild in client.guilds]
    for guild in guilds:
        try:
            await tree.sync(guild=discord.Object(id=guild.id))
            print(f"Synced slash commands to {guild.name}")
        except discord.errors.Forbidden:
            print(f"Failed to sync slash commands to {guild.name}")

    # print "ready" in the console when the bot is ready to work
    print("ready")


def get_date(date_str: str):
    # Date is either "YYYY-MM-DD" or "DD-MM-YYYY" or "DD/MM/YYYY", or the weekday name
    # If it's a weekday name, return the date of the next occurrence of that weekday
    # If it's a date, return the date
    # If it's a date in the wrong format, return None

    weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    weekdays_dutch = ["maandag", "dinsdag", "woensdag", "donderdag", "vrijdag", "zaterdag", "zondag"]

    if date_str is None:
        return date.today()
    elif "/" in date_str:
        # strip the date from the DD/MM/YYYY format
        day, month, year = date_str.split("/")
        return date(int(year), int(month), int(day))
    elif "-" in date_str:
        # strip the date from the YYYY-MM-DD format or DD-MM-YYYY format
        if len(date_str.split("-")[0]) == 4:
            year, month, day = date_str.split("-")
            return date(int(year), int(month), int(day))
        else:
            day, month, year = date_str.split("-")
            return date(int(year), int(month), int(day))
    elif date_str.lower() in weekdays or date_str.lower() in weekdays_dutch:
        # get the date of the next occurrence of the weekday
        weekday = date_str.lower()
        today = date.today()
        if weekday in weekdays:
            weekday_num = weekdays.index(weekday)
        else:
            weekday_num = weekdays_dutch.index(weekday)
        return today + timedelta(days=(weekday_num - today.weekday()) % 7)
    elif date_str.lower() == "tomorrow" or date_str.lower() == "morgen":
        return date.today() + timedelta(days=1)
    elif date_str.lower() == "overmorgen":
        return date.today() + timedelta(days=2)
    elif date_str.lower() == "vandaag" or date_str.lower() == "today":
        return date.today()


@tree.command(name="komida", description="Get the komida menu of the day") #, guilds=list([discord.Object(guild_id) for guild_id in [802509903540912188, 629674224985964579, 693029155398221864, 765945206763028591, 1055830903663898674]])) # Bot test, Master Comp, WINAK, 3e bach, bib vriendjes
async def komida_menu(interaction, location: str, date: str = None):
    """"
    Get the komida menu of the day.

    Parameters
    ----------
    location: str
        The location of the komida. Can be "CST", "CMI", "CGB", "CDE", "HZS" or "ONLINE".
    date: str
        The date of the menu (e.g. 01/12/2022 or tuesday). Can be "YYYY-MM-DD", "DD-MM-YYYY", "DD/MM/YYYY", or the weekday name (e.g. tuesday).
        The default is today. If the date is in the weekend, the menu of the next Monday will be returned.
    """
    # remove quotes from the location
    location = location.replace('"', '')
    assert location.upper() in ["CST", "CMI", "CGB", "CDE", "HZS", "ONLINE"], "Invalid location"

    menu_date = get_date(date)

    # If date is a saturaday or sunday, return the menu for the next monday
    date_changed = False
    if menu_date.weekday() == 5:
        menu_date += timedelta(days=2)
        date_changed = True
    elif menu_date.weekday() == 6:
        menu_date += timedelta(days=1)
        date_changed = True

    view = discord.ui.View()

    if date_changed:
        await interaction.response.send_message(
            f"Komida is closed on weekends. Retrieving the menu for {location} on the next monday ({menu_date.strftime('%d/%m/%Y')})...",
            view=view)
    else:
        await interaction.response.send_message(f"Retrieving the menu for {location} on {menu_date.strftime('%d/%m/%Y')}...", view=view)

    text = komida.get_menu(location, menu_date)
    if text == "":
        text = "No menu found."

    # Update the message with the menu
    await interaction.followup.send(content=text, view=view)


# run the bot
client.run("ENTER YOUR TOKEN")
