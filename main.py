# Program to generate random stratagems, boosters and armour for Helldivers or random operators for Siege
# Remembers player's random generations for a specified number of days, to ensure they are not re-generated,
# then refreshes after this period.
import random
import os
from json import JSONDecodeError
from datetime import datetime as dt, timedelta
import json

# Number of days before stratagem/operator refreshes in player file
BAN_DAYS = 5

# Number of Stratagems per Helldiver Player
NUM_STRATAGEMS = 4

# Common Directories used for the Game
GAME_DIRECTORY = {
    "Game_Data": "./Game_Data.json",
    "Helldivers": "./GameFiles/Helldivers/",
    "Siege": "./GameFiles/Siege"
}

# Dictionary to hold all the game data from file
Helldivers_data = {}
Siege_operators = {}
Banned_pairs = []

# When playing Helldivers, keep track of selected booster amongst different players to ensure no duplicates
hd_selected_boosters = []

# When playing Siege, keep track of selected ops amongst different players to ensure no duplicates
r6_players_selected_ops = {
    "Attackers": [],
    "Defenders": [],
}

"""Retrieves all game data for Helldivers, Siege and Game_Rules from file and writes it to the relevant dictionary.
Returns True if game_data read from file successfully, otherwise returns False."""
def import_game_data():
    global Helldivers_data, Siege_operators, Banned_pairs

    # Attempt to open Game_Data file from Game Directory and read game data into relevant dictionary
    try:
        with open(GAME_DIRECTORY['Game_Data'], 'r') as game_file:
            the_game_data = json.load(game_file)
            Helldivers_data = the_game_data['Helldivers_data']
            Siege_operators = the_game_data['Siege_operators']

            # Check if the_game_data has rules and banned pairs
            if "Game_Rules" in the_game_data and "Banned_Pairs" in the_game_data["Game_Rules"]:
                Banned_pairs = [tuple(pair) for pair in the_game_data["Game_Rules"]["Banned_Pairs"]]
            else:
                Banned_pairs = []

        return True

    # if an errors return False
    except FileNotFoundError:
        print(f"File: {GAME_DIRECTORY['Game_Data']} Not Found")
        return False

    except JSONDecodeError:
        print("File Decode Error. Game_Data file may be corrupted...")
        return False


"""Deletes a stratagem or operator from the Helldivers_data/Siege_operators dictionary.
Takes the game type (Helldivers or Siege as input)."""
def delete_game_data(the_game_type):
    global Helldivers_data, Siege_operators

    # Select the dictionary to use based on users input game_type
    if the_game_type == "Helldivers":
        game_data = Helldivers_data
    elif the_game_type == "Siege":
        game_data = Siege_operators
    # If no valid game type, return to settings menu
    else:
        print("\nInvalid Game. Returning to settings...")
        return

    # Display the categories under the relevant dictionary for players to choose from
    print(f"\n{the_game_type}:\nUnder which category would you like to delete an item: ")
    counter=1
    for the_key in game_data:
        print(f"{counter}: {the_key}")
        counter+= 1

    # Get user to choose which category they want to access (Perform input error correction)
    category = ""
    while category not in game_data:
        category = input("\nPlease type ONLY the category name: ").title()

    # List all the item in the selected category
    print(f"\nWhich item in {the_game_type}: {category} would you like to remove?")
    counter = 1
    for item in game_data[category]:
        print(f"{counter}: {item}")
        counter+= 1

    # user to input which item they wish to delete (perform input error correction)
    item = ""
    while item not in game_data[category]:
        item = input("\nPlease type only the item's NAME: ").title()

    # Request user to confirm their selection (perform input error correction)
    confirm = ""
    while not confirm == 'Y' and not confirm == 'N':
        print(f"\nPlease confirm you would like to remove the following item from {the_game_type} Data: ")
        print(f"{category}: {item}")
        confirm = input(f"\nDelete '{item}' - Yes(Y) or No(N): ").upper()

    # if user confirms, remove item from game_dictionary
    if confirm == 'Y':
        game_data[category].remove(item)
        print(f"\n{item} has been successfully deleted...")
        print(game_data[category])
    # Otherwise return to settings without removing item
    else:
        print(f"\n{item} has NOT been deleted...")


"""Edits a stratagem or operator in the Helldivers_data/Siege_operators dictionary.
Takes the game type (Helldivers or Siege as input)."""
def edit_game_data(the_game_type):
    global Helldivers_data, Siege_operators

    # Select the dictionary to use based on users input game_type
    if the_game_type == "Helldivers":
        game_data = Helldivers_data
    elif the_game_type == "Siege":
        game_data = Siege_operators
    # If no valid game type, return to settings menu
    else:
        print("\nInvalid Game. Returning to settings...")
        return

    # Display the categories under the relevant dictionary for players to choose from
    print(f"\n{the_game_type}:\nUnder which category would you like to edit an item: ")
    counter = 1
    for the_key in game_data:
        print(f"{counter}: {the_key}")
        counter += 1

    # Get user to choose which category they want to access (Perform input error correction)
    category = ""
    while category not in game_data:
        category = input("\nPlease type ONLY the category NAME: ").title()

    # List all the item in the selected category
    print(f"\nWhich item in {the_game_type}: {category} would you like to edit?")
    counter = 1
    for item in game_data[category]:
        print(f"{counter}: {item}")
        counter += 1

    # User to input which item they wish to edit (perform input error correction)
    item = ""
    while item not in game_data[category]:
        item = input("\nPlease type only the item's name: ").title()

    # User to input the new value for the item that they chose to edit (perform input error correction)
    edited_item = ""
    while edited_item == "":
        edited_item = input(f"\nWhat would you like to change {item} to: ")

    # Request user to confirm their final edit (perform input error correction)
    confirm = ""
    while not confirm == 'Y' and not confirm == 'N':
        print(f"\nPlease confirm that you would like to make the following changes in {the_game_type}: {category}: ")
        print(f"FROM {item} TO {edited_item}")
        confirm = input(f"\nConfirm Yes(Y) or No(N): ").upper()

    # If user confirms update game_dictionary by replacing the old value with the new
    if confirm == 'Y':
        the_index = game_data[category].index(item)
        game_data[category][the_index] = edited_item
        print(f"\n{item} has been successfully changed to {edited_item}...")
        print(game_data[category])
    # Otherwise do not change value and return to settings
    else:
        print(f"\n{item} has NOT been changed...")


"""Adds a stratagem or operator to Helldivers_data/Siege_operators dictionary.
Takes the game_type (Helldivers or Siege as input)."""
def add_game_data(the_game_type):
    global Helldivers_data, Siege_operators

    # Select the dictionary to use based on users input game_type
    if the_game_type == "Helldivers":
        game_data = Helldivers_data
    elif the_game_type == "Siege":
        game_data = Siege_operators
    # If no valid game type, return to settings menu
    else:
        print("\nInvalid Game. Returning to settings...")
        return

    # Display the categories under the relevant dictionary for players to choose from
    print(f"\n{the_game_type}:\nUnder which category would you like to add an item: ")
    counter = 1
    for the_key in game_data:
        print(f"{counter}: {the_key}")
        counter += 1

    # Get user to choose which category they want to access (Perform input error correction)
    category = ""
    while category not in game_data:
        category = input("\nPlease type ONLY the category NAME: ").title()

    # User to input the new value that they wish to add to the game (perform input error correction)
    print(f"\nWhat item would you like to add to {the_game_type}: {category}? ")
    new_item = ""
    while new_item == "":
        new_item = input("Type the item's name: ").title()

    # Request user to confirm the new value (perform input error correction)
    confirm = ""
    while not confirm == 'Y' and not confirm == 'N':
        print(f"\nPlease confirm you would like to add the following item to {the_game_type} Data: ")
        print(f"{category}: {new_item}")
        confirm = input(f"\nAdd '{new_item}' - Yes(Y) or No(N): ").upper()

    # If user confirms, add new value to the chosen category in the game_dictionary
    if confirm == 'Y':
        game_data[category].append(new_item)
        print(f"\n{new_item} has been added...")
        print(game_data[category])
    # Otherwise do not add new item and return to settings
    else:
        print(f"\n{new_item} has NOT been added...")


"""Allows a user to view the data in the Helldivers_data/Siege_operators dictionary.
Takes the game type (Helldivers or Siege),
and how the user wants to view data (All, by default, or Specific game data)"""
def view_game_data(the_game_type, view_type):
    global Helldivers_data, Siege_operators

    # Select the dictionary to use based on users input game_type
    if the_game_type == "Helldivers":
        game_data = Helldivers_data
    elif the_game_type == "Siege":
        game_data = Siege_operators
    # If no valid game type, return to settings menu
    else:
        print("\nInvalid Game. Returning to settings...")
        return

    # If user has chosen to view specific categories, Display available categories
    if view_type == "Specific":
        print(f"\n{the_game_type}:\nWhich category would you like to view the items for: ")
        counter = 1
        for the_key in game_data:
            print(f"{counter}: {the_key}")
            counter += 1

        # Get user to choose which category they want to access (Perform input error correction)
        category = ""
        while category not in game_data:
            category = input("\nPlease type ONLY the category NAME: ").title()

        # Display all items in the chosen category
        print(f"\nThe items in {the_game_type} - {category}:\n")
        counter = 1
        for item in game_data[category]:
            print(f"{counter}: {item}")
            counter += 1

        # Request if user would like to view another category as well
        print(f"\nWould you like to view the items in another category for {the_game_type}? ")
        # Perform input error correction on user response
        confirm = ""
        while not confirm == 'Y' and not confirm == 'N':
            confirm = input("Yes (Y) or No (N): ").upper()

        # If user selects Yes, begin process again
        if confirm == 'Y':
            view_game_data(the_game_type, "Specific")

    # If user selects to view all data,
    # Display all data for the game_type in game_dictionary
    else:
        for the_key in game_data:
            print(f"\n{the_key}: ")
            counter = 1
            for item in game_data[the_key]:
                print(f"{counter}. {item}")
                counter+= 1


"""Writes all game data to Game_Data.json file"""
def save_game_data():
    global Helldivers_data, Siege_operators

    # Create a dictionary to hold Helldiver and Siege Dictionaries
    game_data = {
        "Helldivers_data": Helldivers_data,
        "Siege_operators": Siege_operators
    }

    # Write dictionaries to  specified file in Game Directory
    with open(GAME_DIRECTORY['Game_Data'], 'w') as outfile:
        json.dump(game_data, outfile, indent=4)
        print("\nGame_Data.json Successfully Saved...")


"""Checks a specified players file and, 
displays the number and description of the currently available stratagems/operators for that player.
Takes the game type(Helldivers or Siege) and the players name as input.
Displays output to screen."""
def check_player_data(the_game_type, player_name):
    # Update players profile
    update_player_file(player_name, the_game_type)

    # Retrieves player data from a file
    players_data = read_saved_file(player_name, the_game_type)

    # If the player data returned successfully
    if players_data:

        # If the game is helldivers - find the remaining stratagems available to the player
        if the_game_type == "Helldivers":
            # Get a list of all stratagems
            all_stratagems = [val for the_key in Helldivers_data
                              if the_key in {"Orbital", "Eagle", "Supply", "Defensive"} for val in Helldivers_data[the_key]]

            # Get a list of used stratagems from players file
            used_stratagems = [stratagem for dictionary in players_data for stratagem in dictionary['Stratagems']]

            # Get the list of used stratagems with only unique values (no duplicates)
            unique_used_strat = [stratagem for stratagem in all_stratagems if stratagem in used_stratagems]

            # Get the list of remaining stratagems to the player
            remaining_stratagems = [val for val in all_stratagems if val not in used_stratagems]

            # Find the total number of stratagems and the number or remaining stratagems
            total_num_strats = len(all_stratagems)
            num_of_remaining_strats = len(remaining_stratagems)

            # Determine Percent of stratagems used:
            used_strat_percent = round(float((len(unique_used_strat)/total_num_strats) * 100), 2)

            # Output the relevant data to screen
            print(f"\nTotal number of Stratagems in Helldivers: {total_num_strats}")
            print(f"{player_name} has utilised {used_strat_percent}% of all Helldiver Stratagems...\n")
            print(f"{player_name} has the following {num_of_remaining_strats} Stratagems left: ")
            counter = 1
            for stratagem in remaining_stratagems:
                print(f"{counter}. {stratagem}")
                counter+= 1

            return

        # if the game is siege - find the remaining attackers and defenders available to the player
        elif the_game_type == "Siege":
            # Get all the attackers & defenders
            all_attackers = Siege_operators['Attackers']
            all_defenders = Siege_operators['Defenders']

            # Get all the used attackers and defenders for the player
            used_attackers = [attacker for item in players_data for attacker in item['Attackers']]
            used_defenders = [defender for item in players_data for defender in item['Defenders']]

            # Get all the unique used attackers and defenders (no duplicates)
            unique_used_attackers = [attacker for attacker in all_attackers if attacker in used_attackers]
            unique_used_defenders = [defender for defender in all_defenders if defender in used_defenders]

            # Get a list of the remaining attackers and defenders for the player
            remaining_attackers = [attacker for attacker in all_attackers if attacker not in used_attackers]
            remaining_defenders = [defender for defender in all_defenders if defender not in used_defenders]

            # Get the number of attackers and defenders in total,
            # and for the remaining attackers/defenders for the player
            total_num_attackers = len(all_attackers)
            total_num_defenders = len(all_defenders)
            num_remaining_attackers = len(remaining_attackers)
            num_remaining_defenders = len(remaining_defenders)

            # Determine the percent of attackers and defenders used:
            used_attacker_percent = round(float((len(unique_used_attackers) / total_num_attackers) * 100), 2)
            used_defender_percent = round(float((len(unique_used_defenders) / total_num_defenders) * 100), 2)

            # Output the relevant data for both attackers and defenders to screen
            # Attackers Output
            print(f"\nTotal number of Attackers in Siege: {total_num_attackers}")
            print(f"{player_name} has utilised {used_attacker_percent}% of all Siege Attackers...\n")
            print(f"{player_name} has the following {num_remaining_attackers} Attackers left: ")
            counter = 1
            for attacker in remaining_attackers:
                print(f"{counter}. {attacker}")
                counter+= 1

            # Defenders Output
            print(f"\nTotal number of Defenders in Siege: {total_num_defenders}")
            print(f"{player_name} has utilised {used_defender_percent}% of all Siege Defenders...\n")
            print(f"{player_name} has the following {num_remaining_defenders} Defenders left: ")
            counter = 1
            for defender in remaining_defenders:
                print(f"{counter}. {defender}")
                counter+= 1

            return

        # if not valid game type, print error message and return
        else:
            print(f"\n{the_game_type} is an invalid game type. Returning to settings...")
            return

    # if player data is empty, print error message and return
    else:
        print(f"\nNo Player Data was found for {player_name}. Returning to settings...")
        return


""""Allows the user to add, edit, delete or view game data. Used to update Game_Data.json file. 
Additionally, a user can check how many stratagems/operators are currently available to a specified player.
Takes the game type (Helldivers or Siege) as input,
Returns True if a user wishes to continue with the game afterwards, and False otherwise."""
def update_game_data(the_game_type):
    global Helldivers_data, Siege_operators

    # Display Settings options
    print(f"\n{the_game_type.upper()} SETTINGS:")
    print("What settings would you like to use?")
    print(f"1. Add new data to {the_game_type} Game Data")
    print(f"2. Edit existing data in {the_game_type} Game Data")
    print(f"3. Delete existing data in {the_game_type} Game Data")
    print(f"4. View the existing data in {the_game_type} Game Data")
    if the_game_type == "Helldivers":
        print("5. Check the currently available Helldiver stratagems for a specified player")
    else:
        print("5. Check the currently available Siege operators for a specified player")

    # Get users input and perform any input error corrections
    user_response = 0
    while user_response <= 0 or user_response > 5:
        try:
            user_response = int(input("\nEnter only the NUMBER of the option that you wish to perform: "))
        except ValueError:
            print("Incorrect data value. Please input a number from 1 to 5.")

    # Add Game Data and save to Game_Data file
    if user_response == 1:
        add_game_data(the_game_type)
        save_game_data()

    # Edit Game Data and save to Game_Data file
    elif user_response == 2:
        edit_game_data(the_game_type)
        save_game_data()

    # Delete Game Data and save to Game_Data file
    elif user_response == 3:
        delete_game_data(the_game_type)
        save_game_data()

    # View Game Data
    elif user_response == 4:
        print(f"\nWould you like to see data specific to the {the_game_type} categories or all data")

        user_view_type = ""
        while not user_view_type == "All" and not user_view_type == "Specific":
            user_view_type = input("Please type 'All' or 'Specific': ").title()

        view_game_data(the_game_type, user_view_type)

    # Check player data
    elif user_response == 5:
        print("\nInput the player's name you would like to check: ")
        the_players_name = ""
        while the_players_name == "":
            the_players_name = input("Players Name: ")
        check_player_data(the_game_type, the_players_name)

    # Otherwise return to settings
    else:
        print("Invalid response. Returning to game...")
        return False

    # Ask user if they wish to continue in settings or proceed back to game
    print("\n\nWould you like to continue with the Game Settings?")
    continue_in_settings = ""
    while not continue_in_settings == 'Y' and not continue_in_settings == 'N':
        continue_in_settings = input("Type 'Y' for Yes and 'N' for No: ").upper()

    # if user wishes to continue in settings
    if continue_in_settings == 'Y':
        return True
    # otherwise return false
    else:
        return False


"""Writes player's stratagems/operators to a file including date and time.
Takes the game type (Helldivers or Siege) and the list of created players data as input.
Returns a json file for each player"""
def save_player_file(game_type, player_list):

    # Check that game is valid
    if game_type not in GAME_DIRECTORY:
        raise ValueError("Invalid Game. Must be 'Helldivers' or 'Siege'.\n")

    for player in player_list:
        # Creates relevant suffix for game type
        suffix = "HD" if game_type == "Helldivers" else "R6"
        # Complete the file_name
        file_name = f"{player['Name']}_{suffix}.json"

        #Joins the file path from game_dir and file name together
        complete_file_path = os.path.join(GAME_DIRECTORY[game_type], file_name)

        try:
            # Attempt to append new player data to old data
            with open(complete_file_path, "r") as in_file:
                # Load players previous data
                data = json.load(in_file)
                # if data is a dictionary, convert data to a list of dictionaries
                if isinstance(data, dict):
                    data = [data]

        except json.JSONDecodeError:
            print(f"Warning: {complete_file_path} was corrupted. Overwriting it with new data...")
            data = []

        except FileNotFoundError:
            print(f"{player['Name']}'s File not found. Creating new file...\n")
            data = []

        # Append new player data to old data (if error appends to empty data list)
        data.append(player)

        # Convert and send data file to filepath
        with open(complete_file_path, "w") as out_file:
            json.dump(data, out_file, indent=4)


""""Retrieves players data from json file.
Takes the players name and the game type (Helldivers or Siege) as input.
Returns the players full profile."""
def read_saved_file(player_name, game_type):

    # Check that game is valid
    if game_type not in GAME_DIRECTORY:
        raise ValueError("Invalid Game. Must be 'Helldiver' or 'Siege'.\n")

    # Creates relevant suffix for game type
    suffix = "HD" if game_type == "Helldivers" else "R6"
    # Complete the file_name
    file_name = f"{player_name}_{suffix}.json"

    # Joins the file path from game_dir and file name together
    complete_file_path = os.path.join(GAME_DIRECTORY[game_type], file_name)

    # Attempt to retrieve player data
    try:
        with open(complete_file_path, "r") as in_file:
            player_data = json.load(in_file)
    except FileNotFoundError:
        player_data = []
    except JSONDecodeError:
        player_data = []

    return player_data


"""Compares current date to the dates in a players file, dates that are before BAN_DAYS period of time are discarded, 
and the the remaining player dictionary is saved to file.
Takes player name to search for in files and the game type(Siege or Helldivers) as input."""
def update_player_file(player_name, game_type):
    # Get the current date and determine the date that players file refresh
    today = dt.now()
    refresh_date = today - timedelta(days=BAN_DAYS)

    # read players data from file
    player_data = read_saved_file(player_name, game_type)

    if len(player_data) == 0:
        return

    else:
        # Creates a list of player data that has not yet expired
        updated_data = [item for item in player_data if dt.strptime(item["Date"], "%d-%m-%Y") > refresh_date]

        # Check that game is valid
        if game_type not in GAME_DIRECTORY:
            raise ValueError("\nInvalid Game. Must be 'Helldiver' or 'Siege'.\n")

        # Creates relevant suffix for game type
        suffix = "HD" if game_type == "Helldivers" else "R6"
        # Complete the file_name
        file_name = f"{player_name}_{suffix}.json"

        # Joins the file path from game_dir and file name together
        complete_file_path = os.path.join(GAME_DIRECTORY[game_type], file_name)

        with open(complete_file_path, "w") as updated_file:
            json.dump(updated_data, updated_file, indent=4)
        # Prints if update complete
        print(f"\nUpdated {player_name}'s File...")


"""Displays the players name and random stratagems/operators that have been generated in a clear format.
Takes the game (Helldivers or Siege) and the generated player list as input.
Returns the output to screen."""
def display_output(game_type, player_list):
    #If Helldivers display player name, stratagem, Booster and Armour
    if game_type == "Helldivers":
        for item in player_list:
            print(f"\n\nName: {item['Name']}")
            print(f"Stratagems: ")
            counter = 1
            for stratagem in item['Stratagems']:
                print(f"{counter}: {stratagem}")
                counter+=1
            print(f"\nBooster: {item['Booster']}")
            print(f"Armour: {item['Armour']}\n")

    #If Siege display player name, selected attackers, defenders and OT ops
    elif game_type == "Siege":
        for item in player_list:
            print(f"\n\nName: {item['Name']}")
            print("Attackers: ")
            counter = 1
            for attacker in item['Attackers']:
                print(f"{counter}: {attacker}")
                counter+= 1
            print("\nDefenders: ")
            counter = 1
            for defender in item['Defenders']:
                print(f"{counter}: {defender}")
                counter += 1
            print("\nPotential Overtime Operators: ")
            print(f"Overtime Attacker: {item['Overtime'][0]}")
            print(f"Overtime Defender: {item['Overtime'][1]}\n")


"""Checks the generated players stratagem list to see 
if players have been assigned incompatible stratagem combinations from the banned_pairs list. 
If so removes one of the incompatible stratagems and generates a new one.
Takes the players stratagem list and the player's currently unavailable stratagem list as input.
Returns a valid players stratagem list."""
def check_valid_stratagems(player_stratagems, unavailable_stratagems):
    global Banned_pairs

    # For each pair in banned pair list
    for pair in Banned_pairs:

        # If BOTH stratagems from a banned pair in player list
        if all(stratagem in player_stratagems for stratagem in pair):
            # Choose a random stratagem from the pair and remove it
            removed_stratagem = random.choice(pair)
            player_stratagems.remove(removed_stratagem)

            # Add the removed stratagem to the unavailable list
            unavailable_stratagems.append(removed_stratagem)
            # Get a list of all stratagems in helldivers
            all_strats = [val for the_key in Helldivers_data
                              if the_key in {"Orbital", "Eagle", "Supply", "Defensive"} for val in
                              Helldivers_data[the_key]]

            # Create a list of available stratagems, and get its size
            available_strats = [val for val in all_strats
                                if val not in unavailable_stratagems and val not in player_stratagems]
            num_of_avail_strats = len(available_strats)

            # If there is at least one stratagem left in available stratagems, select 1 random stratagem
            if num_of_avail_strats >= 1:
                player_stratagems.append(random.choice(available_strats))
            # If there are not enough stratagems remaining, select from all stratagems
            else:
                # Ensure that the stratagem is not part of the banned pair
                the_strat = random.choice(all_strats)
                while the_strat != removed_stratagem:
                    the_strat = random.choice(all_strats)

                # Add the new valid stratagem to players list
                player_stratagems.append(the_strat)

    return player_stratagems


"""Generates random stratagems for players based on the random type selected by user.
Will check users local file to ensure that the same stratagems are not repeated.
Takes randomness type (complete random or random spread) and the player's name as input.
Returns a random list of stratagems as output"""
def generate_stratagems(game_mode="complete random", player_name=""):
    # Read player data file to check for previously used stratagems
    players_data = read_saved_file(player_name, "Helldivers")

    # Extract all stratagems into a single list
    all_stratagems = [val for the_key in Helldivers_data
                      if the_key in {"Orbital", "Eagle", "Supply", "Defensive"} for val in Helldivers_data[the_key]]

    # Get player's previously used stratagems
    unavailable_stratagems = [stratagem for dictionary in players_data for stratagem in dictionary['Stratagems']]

    # Create a list of player stratagems
    player_stratagems = []

    # COMPLETELY RANDOM SELECTION
    if game_mode == "complete random":
        # If no previous data, pick random stratagems from all helldiver stratagems
        if not players_data:
            player_stratagems = random.sample(all_stratagems, NUM_STRATAGEMS)

        else:
            # Create a list of stratagems from available stratagems that are not in unavailable list
            available_stratagems = [val for val in all_stratagems if val not in unavailable_stratagems]
            num_available_stratagems = len(available_stratagems)

            # If available stratagems is large enough, randomly all stratagems from available stratagems
            if num_available_stratagems >= NUM_STRATAGEMS:
                player_stratagems = random.sample(available_stratagems, NUM_STRATAGEMS)

            # if available stratagems not empty but less than the required stratagems,
            # use all the available stratagems and then randomly select the remainder
            elif 0 < num_available_stratagems < NUM_STRATAGEMS:
                # Get all the available stratagems
                player_stratagems = [stratagem for stratagem in available_stratagems]
                # Calculate the deficit of stratagems
                num_remain_stratagems = NUM_STRATAGEMS - len(player_stratagems)

                # Create a list of all the stratagems NOT including one's already selected
                temp_available_stratagems = [val for val in all_stratagems if val not in player_stratagems]
                # Choose the deficit amount of stratagems from this list
                remain_stratagems = random.sample(temp_available_stratagems, num_remain_stratagems)

                # Extract each stratagem from its list and add to players stratagems
                for stratagem in remain_stratagems:
                    player_stratagems.append(stratagem)

                # Output Notification to player
                print(f"Player {player_name} only had {num_available_stratagems} remaining. "
                      f"All available stratagems have been depleted. Refreshing Stratagems...")

            # Otherwise, if no stratagems available at all, randomly select from all stratagems
            else:
                player_stratagems = random.sample(all_stratagems, NUM_STRATAGEMS)
                print(f"Player {player_name} has exhausted all available stratagems. Refreshing Stratagems...")

        # Check that the chosen stratagems are valid
        player_stratagems = check_valid_stratagems(player_stratagems, unavailable_stratagems)

    # RANDOM SPREAD SELECTION
    elif game_mode == "random spread":
        # Get all stratagem category keys
        all_stratagem_keys = list(Helldivers_data.keys())

        # Exclude helldiver keys that are not relevant to stratagems
        excluded_keys = [the_key for the_key in all_stratagem_keys if the_key == "Boosters" or the_key == "Armour"]

        # List of necessary stratagem keys for random selection
        stratagem_keys = [the_key for the_key in all_stratagem_keys if the_key not in excluded_keys]

        # Select random categories
        random_keys = random.sample(stratagem_keys, NUM_STRATAGEMS)

        #For each key/category get the available stratagems and randomly choose 1 for each category
        for the_key in random_keys:
            # Filter out unavailable stratagems in this category
            available_in_category = [val for val in Helldivers_data[the_key] if val not in unavailable_stratagems]

            # Pick a random available stratagem, or use any stratagem if all have been used
            if available_in_category:
                player_stratagems.append(random.choice(available_in_category))
            else:
                player_stratagems.append(random.choice(Helldivers_data[the_key]))
                print(f"Player {player_name} has exhausted all available stratagems in {the_key} category. "
                      f"Refreshing Stratagems...")

    # If random type incorrect default to completely random
    else:
        print("Invalid Random Type, defaulting to 'complete random'.")
        return generate_stratagems("complete random", player_name)

    return player_stratagems


"""Generates random attacker and defender operators for each match type (standard or quick).
Search player files to ensure that different operators from previous games are selected. 
Ensures that different players within the same match do not get generated the same operators 
(i.e each player's operator list is unique).
Takes two argument for the match type: 's' for Standard (default), or 'q" for quick match, and the player's name.
Returns a dictionary containing attacker, defender and overtime operators"""
def generate_operators(game_mode="standard", player_name=""):
    global r6_players_selected_ops

    #Get all attackers and defenders:
    all_attackers = Siege_operators['Attackers']
    all_defenders = Siege_operators['Defenders']

    # Check which attackers & defenders are available
    player_data = read_saved_file(player_name, "Siege")
    if not player_data:
        available_attackers = all_attackers
        available_defenders = all_defenders

    else:
        # Create a list of attackers and defenders that a player has played recently from players file
        unavailable_attackers = [attacker for the_dict in player_data for attacker in the_dict['Attackers']]
        unavailable_defenders = [defender for the_dict in player_data for defender in the_dict['Defenders']]

        #if selected players not empty:
        if r6_players_selected_ops:
            # Append attackers in selected players to the unavailable attackers
            for attacker in r6_players_selected_ops['Attackers']:
                unavailable_attackers.append(attacker)

            # Append defenders in selected players to the unavailable defenders
            for defender in r6_players_selected_ops['Defenders']:
                unavailable_defenders.append(defender)

        #Create a list of available attackers and defenders for random selection
        available_attackers = [attacker for attacker in all_attackers if attacker not in unavailable_attackers]
        available_defenders = [defender for defender in all_defenders if defender not in unavailable_defenders]

    # Determine how many attackers/defenders to generate
    # If Quick match selected
    if game_mode == "quick":
        num_operators = 2
    # if Standard selected
    elif game_mode == "standard":
        num_operators = 3
    # If error, set to default of Standard
    else:
        print("Invalid match type...Defaulting to 'Standard' Match")
        num_operators = 3

    # Ensure enough attackers and defenders available,
    # otherwise reset to all operators (not including ops already selected by other players)
    if len(available_attackers) < num_operators:
        available_attackers = [attacker for attacker in all_attackers
                               if attacker not in r6_players_selected_ops['Attackers']]
        print(f"Player {player_name} has exhausted all the available Attackers. Refreshing All Attackers...")
    if len(available_defenders) < num_operators:
        available_defenders = [defender for defender in all_defenders
                               if defender not in r6_players_selected_ops['Defenders']]
        print(f"Player {player_name} has exhausted all the available Defenders. Refreshing All Defenders...")

    # Generate attackers & defender from available operators
    attacker_ops = random.sample(available_attackers, num_operators)
    defender_ops = random.sample(available_defenders, num_operators)

    #Append the players attackers and defenders to the player_selected ops
    for attacker in attacker_ops:
        r6_players_selected_ops['Attackers'].append(attacker)

    for defender in defender_ops:
        r6_players_selected_ops['Defenders'].append(defender)

    # Update the list of attackers and defenders for overtime operator selections
    updated_attackers = list(set(available_attackers) - set(attacker_ops) - set(r6_players_selected_ops))
    updated_defenders = list(set(available_defenders) - set(defender_ops) - set(r6_players_selected_ops))

    # if not enough updated attackers,
    # refresh the attackers and remove those that have already been selected
    # for match by player (and other players in the same match)
    if not updated_attackers:
        updated_attackers = [attacker for attacker in all_attackers
                             if attacker not in attacker_ops or attacker not in r6_players_selected_ops['Attackers']]
        print(f"Player {player_name} has exhausted all remaining Attackers. Refreshing All Attackers...")

    # if not enough updated defenders,
    # refresh the defenders and remove those that have already been selected
    # for match by player (and other players in the same match)
    if not updated_defenders:
        updated_defenders = [defender for defender in all_defenders
                             if defender not in defender_ops or defender not in r6_players_selected_ops['Defenders']]
        print(f"Player {player_name} has exhausted all remaining Defenders. Refreshing All Defenders...")

    # Generate 1 random attacker from the updated attacker pool
    ot_attacker = random.sample(updated_attackers, 1)[0]
    # Append OT Attacker to player_selected list
    r6_players_selected_ops['Attackers'].append(ot_attacker)

    # Generate 1 random defender from the updated defender pool
    ot_defender = random.sample(updated_defenders, 1)[0]
    # Append OT Defender to player_selected list
    r6_players_selected_ops['Defenders'].append(ot_defender)

    # assign OT operators to list
    overtime_ops = [ot_attacker, ot_defender]

    # Create a dictionary of selected attackers, defenders and overtime ops
    operator_dict = {
        "Attackers": attacker_ops,
        "Defenders": defender_ops,
        "Overtime": overtime_ops
    }

    return operator_dict


"""Generates a player profile for each player based on game type(Helldivers or Siege).
Checks for a previous player profile, and updates as necessary,
Creates player dictionaries, uses Generate Strategem/Operators to retrieve random stratagems/operators. 
Finally, sends to DisplayOutput and Saves to player's local file.
Takes number of players, game type and game mode as input"""
def create_players(num_players, game_type, game_mode):
    print("Input the Player Names: \n")
    player_names = [input(f"Player {num+1}: ") for num in range(0, num_players)]

    #Update player files
    for name in player_names:
        update_player_file(name, game_type)

    # Create date and time objects
    today = dt.now()
    date = today.date()
    time = today.time()

    # Reformat date and time:
    the_date = date.strftime("%d-%m-%Y")
    the_time = time.strftime("%HH%M")

    #Create a list of player dictionaries for writing to file
    player_list = []

    # If the user is playing Helldivers
    if game_type == "Helldivers":
        for player in player_names:
            # Get the available boosters from file
            available_boosters = [booster for booster in Helldivers_data['Boosters']
                                  if booster not in hd_selected_boosters]

            # Select a random booster from available boosters, and add it to the hd_selected_boosters
            random_booster = random.choice(available_boosters)
            hd_selected_boosters.append(random_booster)

            player_dict = {
                "Name": player,
                "Stratagems": generate_stratagems(game_mode, player),
                "Booster": random_booster,
                "Armour": random.choice(Helldivers_data['Armour']),
                "Date": the_date,
                "Time": the_time,
            }
            player_list.append(player_dict)

    # If the user is playing Siege
    elif game_type == "Siege":
        for player in player_names:
            player_ops = generate_operators(game_mode, player)
            the_attackers = [val for val in player_ops['Attackers']]
            the_defenders = [val for val in player_ops['Defenders']]
            the_overtime = [val for val in player_ops['Overtime']]
            player_dict = {
                "Name": player,
                "Attackers": the_attackers,
                "Defenders": the_defenders,
                "Overtime": the_overtime,
                "Date": the_date,
                "Time": the_time,
            }
            player_list.append(player_dict)

    # Outputs players random choices to screen
    display_output(game_type, player_list)

    # Saves players current random choices to screen
    save_player_file(game_type, player_list)



#Extract Game Data from File
successful_data_import = import_game_data()

# If game data successfully read from file, continue with Random Game Generator
if successful_data_import:
    game_continues = True
# Otherwise do not proceed with Random Game Generator
else:
    print("Unable to import Game_Data from file. Aborting Random Game Generator...")
    game_continues = False

#Begin Random Game Generator
while game_continues:
    print("GAME RANDOM SELECTOR: \n")

    # Select which game to generate random content
    print("Which Game are you playing?")
    game = input("Helldivers(HD) or Siege(S): ").upper()
    # Perform input error correction
    while not game == "HD" and not game == "S" and not game == "SETTINGS":
        print("\nInvalid selection. \nPlease input 'HD' for Helldivers and 'S' for Siege")
        game = input("Helldivers(HD) or Siege(S): ").upper()
    # Convert user input to function related names:
    if game == "HD":
        the_game = "Helldivers"
    elif game == "S":
        the_game = "Siege"
    else:
        the_game = "Settings"

    # SETTINGS
    if the_game == "Settings":
        continue_settings = True
        # User can input settings for as long as they wish
        while continue_settings:
            # User to input which game they would like to access settings for
            print("Which Game would you like to access the settings for: ")
            # Perform user input correction for settings
            settings_choice = ""
            while not settings_choice == "Helldivers" and not settings_choice == "Siege":
                print("\nHelldivers or Siege")
                settings_choice = input("Please type the game name out in full: ").title()

            # If the user has selected to continue with settings,
            # continue settings will be True otherwise exits loop
            continue_settings = update_game_data(settings_choice)

        # Ask user if they wish to continue with game or exit application
        print("\n\nWould you like to continue with the Random Game Generation?")
        proceed_to_game = ""
        while not proceed_to_game == 'Y' and not proceed_to_game == 'N':
            proceed_to_game = input("Type 'Y' for Yes and 'N' for No: ").upper()

        # if user does not wish to proceed, exit application
        if proceed_to_game == 'N':
            game_continues = False
            break
        # Otherwise, proceed with Random Game Generation
        else:
            # Select which game to generate random content
            print("Which Game are you playing:\n")
            game = input("Helldivers(HD) or Siege(S): ").upper()
            # Perform input error correction
            while not game == "HD" and not game == "S":
                print("\nInvalid selection. \nPlease input 'HD' for Helldivers and 'S' for Siege")
                game = input("Helldivers(HD) or Siege(S): ").upper()
            # Convert user input to function related names:
            if game == "HD":
                the_game = "Helldivers"
            else:
                the_game = "Siege"


    # GAME TYPES:
    the_game_mode = ""
    number_players = 0

    # HELLDIVERS GAME
    if the_game == "Helldivers":
        # Select Players for Helldivers, ensure valid input
        while number_players <= 0 or number_players > 4:
            try:
                # Input number of players
                print("\nPlease enter the number of players in this session (Helldivers 1 - 4 players): ")
                number_players = int(input("How many players: "))
            except ValueError:
                print("Incorrect data type. Please input a number greater than 0 and less than 5.")

        # Select which form of randomness
        print("\nWould you like to have complete randomness or random across the different stratagem categories?")
        the_type = input("Complete randomness(c) or Random Spread(r): ").lower()
        # game type input error correction
        while not the_type == "c" and not the_type == "r":
            print("\nInvalid randomness type.\nPlease enter 'c' for Complete Randomness or 'r' for a Random Spread.")
            the_type = input("Complete randomness(c) or Random Spread(r): ").lower()
        # Convert input
        if the_type == "c":
            the_game_mode = "complete random"
        else:
            the_game_mode = "random spread"


    # SIEGE GAME
    elif the_game == "Siege":
        # Select players for Siege, ensure valid input:
        while number_players <= 0 or number_players > 5:
            try:
                # Input number of players
                print("\nPlease enter the number of players in this session (Siege 1 - 5 players): ")
                number_players = int(input("How many players: "))
            except ValueError:
                print("Incorrect data type. Please input a number greater than 0 and less than 5.")

        # Determine the Siege match type
        print("\nMatch Type: ")
        siege_match_type = input("Standard(s) or Quick Match (q): ").lower()
        # Siege match type input error correction
        while not siege_match_type == "s" and not siege_match_type == "q":
            print("\nInvalid match type.\nPlease enter 'q' for Quick Match or 's' for Standard: ")
            siege_match_type = input("Standard(s) or Quick Match (q): ").lower()
        # Convert input:
        if siege_match_type == "s":
            the_game_mode = "standard"
        else:
            the_game_mode = "quick"


    # If game type not HELLDIVERS, SIEGE or SETTINGS, end the program.
    else:
        print("Invalid game type. Exiting Program...")
        game_continues = False
        break

    # Create player dict and generate stratagems/operators for match
    create_players(number_players, the_game, the_game_mode)

    # Reset the hd_selected_boosters list for Helldivers to empty/default
    hd_selected_boosters = []

    # Reset the player_selection_ops dict for Siege to empty/default
    for key in r6_players_selected_ops:
        r6_players_selected_ops[key] = []

    # Request user if they wish to continue with game generator or exit
    # Perform user input correction
    print("\nWould you like to continue to generate more random game content?")
    user_continue = ""
    while not user_continue == 'C' and not user_continue == 'X':
        user_continue = input("Type 'C' to Continue or 'X' to Exit: ").upper()

    # if game continues use new lines for extra space
    if user_continue == "C":
        print("\n\n\n\n\n")
    # Otherwise, end program.
    else:
        game_continues = False
        break


print("\n\nend of program".upper())
