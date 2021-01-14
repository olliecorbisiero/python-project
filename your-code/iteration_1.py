
#latest version
import time
import random
import winsound


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

python_weapon = {
    "name": "python to defeat david henriques",
    "type": "weapon",
    "target": david_henriques,
}
sql_weapon = {
    "name": "sql to defeat jose pereira",
    "type": "weapon",
    "target": jose_pereira,
}
job_weapon = {
    "name": "job to defeat catarina costa",
    "type": "weapon",
    "target": catarina_costa,
}
certification_weapon = {
    "name": "certification to defeat munique martins",
    "type": "weapon",
    "target": munique_martins,
}
your_desk = {
    "name": "your desk",
    "type": "furniture",
}
your_chair = {
    "name": "your chair",
    "type": "furniture",
}
teacher_whiteboard = {
    "name": "teacher whiteboard",
    "type": "furniture",
}
stylish_plant = {
    "name": "stylish plant",
    "type": "furniture",
}

monster_energy_can = {
    "name": "monster energy can",
    "type": "furniture",
}

couch = {
    "name": "couch",
    "type": "furniture",
}

projector = {
    "name": "projector",
    "type": "furniture",
}

fruit_bowl = {
    "name": "fruit bowl",
    "type": "furniture",
}
espresso_machine = {
    "name": "espresso machine",
    "type": "furniture",
}

ping_pong_table = {
    "name": "ping pong table",
    "type": "furniture",
}

data_analytics = {
    "name": "data analytics",
    "type": "room",
}
hallway= {
    "name": "hallway",
    "type": "room",
}
career_room= {
    "name": "career room",
    "type": "room",
}
kitchen = {
    "name": "kitchen",
    "type": "room",
}
balcony = {
  "name": "balcony"
}
all_furniture = [your_desk, your_chair, teacher_whiteboard, stylish_plant, monster_energy_can, couch, projector, espresso_machine, fruit_bowl, ping_pong_table]
all_rooms = [data_analytics, hallway, career_room, kitchen, balcony]
all_weapons = [python_weapon, sql_weapon, job_weapon, certification_weapon]
all_bosses = [david_henriques, jose_pereira, catarina_costa, munique_martins]

DA = ["your desk", "your chair", "teacher whiteboard"]
HW = ["stylish plant", "monster energy can"]
CR = ["couch", "projector"]
K = ["fruit bowl", "espresso machine","ping pong table"]

# define which items/rooms are related

object_relations = {
    #room
    "data analytics": [your_desk, your_chair, teacher_whiteboard, david_henriques],
    "hallway": [stylish_plant, monster_energy_can, david_henriques, catarina_costa, jose_pereira],
    "career room": [couch, projector, catarina_costa],
    "kitchen": [fruit_bowl, espresso_machine,ping_pong_table,jose_pereira, munique_martins],

    #object with key
    random.choice(DA): [python_weapon],
    random.choice(HW): [job_weapon],
    random.choice(CR): [sql_weapon],
    random.choice(K): [certification_weapon],

    #outside
    "balcony": [munique_martins],
    #door
    "david henriques": [data_analytics, hallway],
    "catarina costa": [hallway, career_room],
    "jose pereira": [hallway, kitchen],
    "munique martins": [kitchen, balcony]
}



# define game state. Do not directly change this dict.
# Instead, when a new game starts, make a copy of this
# dict and use the copy to store gameplay state. This
# way you can replay the game multiple times.


INIT_GAME_STATE = {
    "current_room": data_analytics,
    "weapons_collected": [],
    "target_room": balcony
}

start_time = time.time()
time_limit = start_time + 180

def time_check():
  current_time = time.time()
  if current_time > time_limit:
    print("time up, no tech job for you")
    exit()

def leaderboard_add():
  score = time_limit - time.time()
  name = input("congrats you have graduated, enter your name for the leaderboard:")
  total = str(name) + ": " + str(score)
  return total

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
        "You have made the life changing decision to attend Ironhack, however you have been enjoying Lisbon a little too much. \nYou wake up at your desk and look at your watch, you have three minutes until graduation! \nNavigate the campus and acquire the necessary digital weapons to land your dream job in the tech-ecosystem. \nGood luck making it past the staff!")
    play_room(game_state["current_room"])

    
def play_room(room):
    """
    Play a room. First check if the room being played is the target room.
    If it is, the game will end with success. Otherwise, let player either
    explore (list all items in this room) or examine an item found here.
    """
    game_state["current_room"] = room
    winsound.PlaySound('escape_ironhack.wav', winsound.SND_ASYNC)
    if (game_state["current_room"] == game_state["target_room"]):
        new = leaderboard_add()
        add = new + '\n'
        text_file = open("leaderboard.txt", "a")
        text_file.write(add)
        text_file.close()
    else:
        print("You are now in " + room["name"])
        intended_action = input("What would you like to do? Type 'explore' or 'examine'?").strip()
        if intended_action == "explore":
            time_check()
            explore_room(room)
            play_room(room)
        elif intended_action == "examine":
            time_check()
            examine_item(input("What would you like to examine?").strip())
        else:
            print("Not sure what you mean. Type 'explore' or 'examine'.")
            play_room(room)
        linebreak()

def explore_room(room):
    """
    Explore a room. List all items belonging to this room.
    """
    time_check()
    items = [i["name"] for i in object_relations[room["name"]]]
    print("You explore the room. This is " + room["name"] + ". You find " + ", ".join(items))

def get_next_room_of_boss(boss, current_room):
    """
    From object_relations, find the two rooms connected to the given boss.
    Return the room that is not the current_room.
    """
    time_check()
    connected_rooms = object_relations[boss["name"]]
    winsound.PlaySound('defeat_boss.wav', winsound.SND_ASYNC)
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
    time_check()
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
                    output += "You are victorious!"
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

