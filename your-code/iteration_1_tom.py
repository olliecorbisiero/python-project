# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#change
# define rooms and items
david_henriques = {
    "name": "david henriques",
    "type": "boss",
}
jose_pereira = {
    "name": "jose pereira",
    "type": "boss",
}
munique_martins = {
    "name": "munique martins",
    "type": "boss",
}
catarina_costa = {
    "name": "catarina costa",
    "type": "boss",
}
couch = {
    "name": "couch",
    "type": "furniture",
}
piano = {
    "name": "piano",
    "type": "furniture",
}
queen_bed = {
    "name": "queen bed",
    "type": "furniture",
}
double_bed = {
    "name": "double bed",
    "type": "furniture",
}
dresser = {
    "name": "dresser",
    "type": "furniture",
}
dining_table = {
    "name": "dining table",
    "type": "furniture",
}
python_weapon = {
    "name": "weapon for david henriques",
    "type": "weapon",
    "target": david_henriques,
}
sql_weapon = {
    "name": "weapon for jose pereira",
    "type": "weapon",
    "target": jose_pereira,
}
job_weapon = {
    "name": "weapon for catarina costa",
    "type": "weapon",
    "target": catarina_costa,
}
certification_weapon = {
    "name": "weapon for munique martins",
    "type": "weapon",
    "target": munique_martins,
}
game_room = {
    "name": "game room",
    "type": "room",
}
bedroom_1 = {
    "name": "bedroom 1",
    "type": "room",
}
bedroom_2 = {
    "name": "bedroom 2",
    "type": "room",
}
living_room = {
    "name": "living room",
    "type": "room",
}
outside = {
  "name": "outside"
}
all_furniture = [couch, piano, queen_bed, double_bed, dresser, dining_table]
all_weapons = [python_weapon, sql_weapon, job_weapon, certification_weapon]
all_rooms = [game_room, bedroom_1, bedroom_2, living_room, outside]
all_bosses = [david_henriques, jose_pereira, catarina_costa, munique_martins]
# define which items/rooms are related
object_relations = {
    #room
    "game room": [couch, piano, david_henriques],
    "bedroom 1": [queen_bed, david_henriques, catarina_costa, jose_pereira],
    "bedroom 2": [double_bed, dresser, catarina_costa],
    "living room": [dining_table, jose_pereira, munique_martins],
    #object with weapon
    "piano": [python_weapon],
    "queen bed": [job_weapon],
    "double bed": [sql_weapon],
    "dresser": [certification_weapon],
    #outside
    "outside": [munique_martins],
    #boss
    "david henriques": [game_room, bedroom_1],
    "jose pereira": [bedroom_1, bedroom_2],
    "catarina costa": [bedroom_1, living_room],
    "munique martins": [living_room, outside]
}
# define game state. Do not directly change this dict.
# Instead, when a new game starts, make a copy of this
# dict and use the copy to store gameplay state. This
# way you can replay the game multiple times.
INIT_GAME_STATE = {
    "current_room": game_room,
    "weapons_collected": [],
    "target_room": outside
}
def linebreak():
    """
    Print a line break
    """
    print("\n\n")
def start_game():
    """
    Start the game
    """
    print(
        "You wake up on a couch and find yourself in a strange house with no windows which you have never been to before. You don't remember why you are here and what had happened before. You feel some unknown danger is approaching and you must get out of the house, NOW!")
    play_room(game_state["current_room"])
def play_room(room):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either
    explore (list all items in this room) or examine an item found here.
    """
    game_state["current_room"] = room
    if (game_state["current_room"] == game_state["target_room"]):
        print("Congrats! You escaped the room!")
    else:
        print("You are now in " + room["name"])
        intended_action = input("What would you like to do? Type 'explore' or 'examine'?").strip()
        if intended_action == "explore":
            explore_room(room)
            play_room(room)
        elif intended_action == "examine":
            examine_item(input("What would you like to examine?").strip())
        else:
            print("Not sure what you mean. Type 'explore' or 'examine'.")
            play_room(room)
        linebreak()
def explore_room(room):
    """
    Explore a room. List all items belonging to this room.
    """
    items = [i["name"] for i in object_relations[room["name"]]]
    print("You explore the room. This is " + room["name"] + ". You find " + ", ".join(items))
def get_next_room_of_boss(boss, current_room):
    """
    From object_relations, find the two rooms connected to the given boss.
    Return the room that is not the current_room.
    """
    connected_rooms = object_relations[boss["name"]]
    for room in connected_rooms:
        if (not current_room == room):
            return room
def examine_item(item_name):
    """
    Examine an item which can be a boss or furniture.
    First make sure the intended item belongs to the current room.
    Then check if the item is a boss. Tell player if the weapon hasn't been
    collected yet. Otherwise ask player if they want to go to the next
    room. If the item is not a boss, then check if it contains weapons.
    Collect the weapon if found and update the game state. At the end,
    play either the current or the next room depending on the game state
    to keep playing.
    """
    current_room = game_state["current_room"]
    next_room = ""
    output = None
    for item in object_relations[current_room["name"]]:
        if (item["name"] == item_name):
            output = "You examine " + item_name + ". "
            if (item["type"] == "boss"):
                have_weapon = False
                for weapon in game_state["weapons_collected"]:
                    if (weapon["target"] == item):
                        have_weapon = True
                if (have_weapon):
                    output += "You killed it with the weapon you have."
                    next_room = get_next_room_of_boss(item, current_room)
                else:
                    output += "It is being protected and you don't have the weapon."
            else:
                if (item["name"] in object_relations and len(object_relations[item["name"]]) > 0):
                    item_found = object_relations[item["name"]].pop()
                    game_state["weapons_collected"].append(item_found)
                    output += "You find " + item_found["name"] + "."
                else:
                    output += "There isn't anything interesting about it."
            print(output)
            break
    if (output is None):
        print("The item you requested is not found in the current room.")
    if (next_room and input("Do you want to go to the next room? Enter 'yes' or 'no'").strip() == 'yes'):
        play_room(next_room)
    else:
        play_room(current_room)
        
game_state = INIT_GAME_STATE.copy()
start_game()