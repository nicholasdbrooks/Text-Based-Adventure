import classes.player_class as player_class
import textwrap as tr
import random
import json

# initialize command list, direction list, room list
commands = ['go', 'enter', 'quit', 'get', 'inventory', 'drop', 'look', 'items', 'take', 'insert', 'open', 'pull',
            'unlock', 'dig', 'uncover', 'help', 'savegame', 'loadgame']
multi_commands = {'pick': 'up', 'put': 'down', 'items': 'here', 'input': 'code'}
item_commands = ['use', 'try', 'insert', 'pull', 'unlock']
directions = ['north', 'south', 'east', 'west', 'up', 'down']
rooms = ["foyer", "office", "library", "kitchen", "backyard", "graveyard", "hallway", "bathroom", "attic"]
multi_rooms = {'furnace': 'room', 'storage': 'room', 'music': 'room', 'dining': 'room',
               'guest': 'bedroom', 'master': 'bedroom'}
exits = ["passageway"]
multi_exits = {"northern": "exit", "eastern": "archway", "southern": "staircase", "open": "door", "glass": "doors", "fancy": "doorway", "french": "doors", "iron": "gate", "brick": "archway", "western": "archway"}
multi_items = {'knife': 'block', 'metal': 'door', 'coin': 'slot', 'square': 'tombstone', 'oval': 'tombstone',
               'large': 'bed', 'fire': 'poker', 'piano': 'cartridge', 'cartridge': 'slot', 'tool': 'shed'}
vowels = ["a", "e", "i", "o", "u"]
syn_check = False


def printw(text) -> str:
    # @ params: text to print
    # @ return: none
    # prints text wrapped to a specified width

    paragraphs = text.splitlines()
    textOut = "\n".join([tr.fill(p, 100, replace_whitespace=False) for p in paragraphs])
    print(textOut)

# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------
#
# get input from the player for opening the safe
def get_safe_input() -> bool:
    # @ return: True if the player enters the correct code (AEFC), false otherwise
    # gets input from the player for the safe combination
    safe_code = input("Enter a 4 character combination: ").lower()
    print("")
    if safe_code == 'aefc':
        return True
    else:
        return False
#
#
# ----------------------------------------------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------------------------------------------

def get_input() -> str:
    # @ params: none
    # @ return: string of the command entered by the player
    # gets input from the player on where to go
    command = input("\nWhat would you like to do? ").lower()
    return command

def generate_random_phrase():
    phrases = ["A strong wind poicks up outside, but otherwise nothing changes.",
    "There is a strange noise coming from the walls. Mice, maybe? Who knows. Regardless your actions seem to have had no effect.",
    "Nothing happens. You're starting to feel thoroughly spooked by the house's oppressive darkness.",
    "Nothing changes. The house is eerily quiet.",
    "Nothing happens. You feel jumpy and know Dr. Peters wouldn't like this one bit."]

    print(phrases[random.randint(0,len(phrases)-1)])
    return


def parse_inputs(player_input, game_items, player, game_rooms) -> dict:
    # @ params: player_input - input gotten from player
    # @ return: dictionary - {'command': command, 'direction': direction, 'room': room}
    input_list = player_input.split()
    num_input = len(input_list)

    # initialize command, direction, room
    command = ''
    direction = ''
    room = ''
    item = ''
    item2 = ''

    global syn_check

    # for debugging: print(f'room current items: {game_rooms[player.get_location()].current_items}')
    # for debugging: print(f'current player inventory: {player.view_inventory()}')
    # check if the first command is the word 'go' or 'enter'
    # can later be expanded to check for all command verbs
    for i in range(0, num_input):
        if input_list[i] in commands:
            command = input_list[i]
        elif input_list[i] in item_commands:
            command = input_list[i]
        # handle multi-word commands
        elif input_list[i] in multi_commands:
            if len(input_list) > 1:
                if input_list[i + 1] == multi_commands.get(input_list[i]):
                    command = input_list[i] + ' ' + input_list[i + 1]
        elif input_list[i] in directions:
            direction = input_list[i]

        elif input_list[i] in rooms or input_list[i] in multi_rooms:
            room = input_list[i]
            # handle multi-word rooms
            if input_list[i] in multi_rooms:
                if input_list[i + 1] == multi_rooms.get(input_list[i]):
                    room = input_list[i] + ' ' + input_list[i + 1]
            
        elif input_list[i] in exits or input_list[i] in multi_exits:
            exit = ''
            if input_list[i] in exits: exit = input_list[i]
            if i+1 < len(input_list):
                if input_list[i + 1] == multi_exits.get(input_list[i]):
                    exit = input_list[i] + ' ' + input_list[i + 1]
            for g_room in game_rooms:
                for g_direction in game_rooms[g_room].exits[0]:
                    if exit in game_rooms[g_room].exits[0][g_direction] and game_rooms[g_room].exits[0][g_direction][0] != player.get_location(): 
                        room = game_rooms[g_room].exits[0][g_direction][0]

        if input_list[i] in game_items or input_list[i] in multi_items:
            if input_list[i] in multi_items:
            # if item is a multi-item
                if i + 1 < len(input_list) and input_list[i + 1] == multi_items.get(input_list[i]):
                    # if the input is either in the same room as the character or in their inventory
                    if (input_list[i] + ' ' + input_list[i + 1] in game_rooms[
                        player.get_location()].current_items) or (
                            input_list[i] + ' ' + input_list[i + 1] in player.view_inventory()):
                        if item == '':
                            item = input_list[i] + ' ' + input_list[i + 1]
                        else:
                            item2 = input_list[i] + ' ' + input_list[i + 1]
                    else:
                        print_multi_item_access(input_list[i], input_list[i+1])
                # otherwise we have a single item that is part of a multi-item or a synonym
                # want to address game item but pass on synonym
                elif input_list[i] in game_items:
                    if (input_list[i] in game_rooms[player.get_location()].current_items) or (
                            input_list[i] in player.view_inventory()):
                        if item == '':
                            item = input_list[i]
                        else:
                            item2 = input_list[i]
                    else:
                        print_single_item_access(input_list[i])
                
                else: syn_check = True
                            
            # otherwise it is just one word or a synonym
            elif input_list[i] in game_items:
                if (input_list[i] in game_rooms[player.get_location()].current_items) or (
                        input_list[i] in player.view_inventory()):
                    if item == '':
                        item = input_list[i]
                    else:
                        item2 = input_list[i]
                else:
                    print_single_item_access(input_list[i])
                    syn_check = True

            if item != '':
                # check every input to see if it is a verb for first item
                for j in range(0, num_input):
                    # for item-specific commands that are not in the command list
                    if input_list[j] in game_items[item].verbs[0]:
                        printw(game_items[item].verbs[0][input_list[j]]["text"])
                        # ----------------------------------------------------------------------------------------------
                        # ----------------------------------------------------------------------------------------------
                        #
                        # if there is a 'flag' command to be executed, execute said command
                        if game_items[item].verbs[0][input_list[j]]["flag"]:
                            exec(str(game_items[item].verbs[0][input_list[j]]["flag"][0]))
                        #
                        #
                        # ----------------------------------------------------------------------------------------------
                        # ----------------------------------------------------------------------------------------------
                        # set command to bogus symbol so we know command has been executed
                        command = '@'
                # if command is still empty after all this, they entered something invalid
                if command == '':
                    print("It seems you can't do that.")
                    command = '@'    

        # we only want to check synonyms if we have no item found
        # or if parser suspects it was given synonym inside of multi-word
        if item == '' or item2 == '': syn_check = True 
        # check for item synonyms if the item is not in the room or in player inventory
        if syn_check:
            # check room
            for j in game_rooms[player.get_location()].current_items:
                # check if two words in a row have an item synonym
                if (i + 1 < len(input_list)) and (input_list[i] in game_items[j].synonyms and input_list[i+1] in game_items[j].synonyms):
                    if (game_items[j].name in game_rooms[player.get_location()].current_items) or (
                        game_items[j].name in player.view_inventory()):
                        if item == '':
                            item = game_items[j].name 
                        else:
                            item2 = game_items[j].name
                    else:
                        print_multi_item_access(input_list[i], input_list[i+1])

                # check if one word has an item synonym
                elif input_list[i] in game_items[j].synonyms:
                    if (game_items[j].name in game_rooms[player.get_location()].current_items) or (
                        game_items[j].name in player.view_inventory()):
                        if item == '':
                            item = game_items[j].name
                        else:
                            item2 = game_items[j].name
                    else:
                        print_single_item_access(input_list[i])
            # check player inventory
            for j in player.view_inventory():
                # check if two words in a row have an item synonym
                if (i + 1 < len(input_list)) and (input_list[i] in game_items[j].synonyms and input_list[i+1] in game_items[j].synonyms):
                    if (game_items[j].name in game_rooms[player.get_location()].current_items) or (
                        game_items[j].name in player.view_inventory()):
                        if item == '':
                            item = game_items[j].name 
                        else:
                            item2 = game_items[j].name
                    else:
                        print_multi_item_access(input_list[i], input_list[i+1])

                # check if one word has an item synonym
                elif input_list[i] in game_items[j].synonyms:
                    if (game_items[j].name in game_rooms[player.get_location()].current_items) or (
                        game_items[j].name in player.view_inventory()):
                        if item == '':
                            item = game_items[j].name
                        else:
                            item2 = game_items[j].name
                    else:
                        print_multi_item_access(input_list[i], input_list[i+1])
            
            if item != '' and command != '@':
                # check every input to see if it is a verb for first item
                for j in range(0, num_input):
                    # for item-specific commands that are not in the command list
                    if input_list[j] in game_items[item].verbs[0]:
                        printw(game_items[item].verbs[0][input_list[j]]["text"])
                        # ----------------------------------------------------------------------------------------------
                        # ----------------------------------------------------------------------------------------------
                        #
                        # if there is a 'flag' command to be executed, execute said command
                        if game_items[item].verbs[0][input_list[j]]["flag"]:
                            exec(str(game_items[item].verbs[0][input_list[j]]["flag"][0]))
                        #
                        #
                        # ----------------------------------------------------------------------------------------------
                        # ----------------------------------------------------------------------------------------------
                        # set command to bogus symbol so we know command has been executed
                        command = '@'
                # if command is still empty after all this, they entered something invalid
                if command == '':
                    print("It seems you can't do that.")
                    command = '@'
            
            # reset
            syn_check = False

    # for debugging: print({'command': command, 'direction': direction, 'room': room, 'item': item, 'item2': item2})
    return {'command': command, 'direction': direction, 'room': room, 'item': item, 'item2': item2}



def print_single_item_access(input):
    if input[0].lower() not in vowels:
        print(f"You don't have access to a {input}")
    else:
        print(f"You don't have access to an {input}") 

def print_multi_item_access(input1, input2):
    if input1[0].lower() not in vowels:
        print(f"You don't have access to a {input1} {input2}")
    else:
        print(f"You don't have access to an {input1} {input2}") 



def has_direction_exit(direction, game_rooms, player) -> bool:
    # @ params: direction - the direction input by the player
    # @ return: bool - True if room has an exit in that direction, false otherwise
    if direction in game_rooms[player.get_location()].exits[0]:
        return True
    return False


def has_room_exit(room, game_rooms, player) -> bool:
    # @ params: room - the room input by the player
    # @ return: bool - True if room has that given room as an exit, false otherwise
    directions = ['north', 'south', 'east', 'west', 'up', 'down']
    for direction in directions:
        if direction in game_rooms[player.get_location()].exits[0]:
            if game_rooms[player.get_location()].exits[0][direction][0] == room:
                return True
    return False


def display_location(room):
    print('\n----------------------------------------------------------------------------------------------------')
    printw('Current location: ' + room + '\n')
    print('----------------------------------------------------------------------------------------------------\n')


def parser_read_input(player, game_rooms, game_items, puzzle_items, ascii_dict):
    # get input from the player
    player_input = get_input()
    print("")

    # parse the input into:
    #   command (i.e. go, enter, quit)
    #   direction (i.e. NSEW, up, down)
    #   room (i.e. library, dining room, etc.)
    #   item (i.e. letter, cartridge, etc.)
    # parsed_input format: {'command': command, 'direction': direction, 'room': room, 'item': item, 'item2': item2}
    parsed_input = parse_inputs(player_input, game_items, player, game_rooms)

    # exit the program if the player entered quit
    if parsed_input['command'] == 'quit':
        exit()
            
    # list allowed verbs
    if parsed_input['command'] == 'help':
        if parsed_input['item'] != '':
            if parsed_input['item'] in game_items:
                for key in game_items[parsed_input['item']].verbs[0]:
                    print(key)
                for puzzle in puzzle_items:
                    if parsed_input['item'] in puzzle_items[puzzle].key_item:
                        for key_command in puzzle_items[puzzle].key_command:
                            print(key_command)
            else: 
                print("Item not found.")
        else:
            printw("Allowed verbs:\nuse\ntry\ngo\nenter\nquit\ninventory\ndrop\nput down\ntake\nget\npick up\ntouch\nsmell\nhelp")
            printw("For more details on item-related commands, type 'help [item name]'")
        return

    #--------------------------------------------------------
    # save game
    elif parsed_input["command"] == 'savegame':

        # build dictionary of items and their locations
        item_locs = {}
        for item in game_items:
            item_locs[item] = game_items[item].current_loc

        # build dictionary of data to save
        save_data = {
            'current_location': player.get_location(),
            'locs_visited': player.get_locs_visited(),
            'inventory': player.get_inventory(),
            'item_locs': item_locs,
            'cur_puzzle': player.get_current_puzzle(),
            'painting_status': player.get_painting_status()
        }

        # save the dictionary to a file
        try: 
            with open("saved_data.json", "w") as outfile:
                json.dump(save_data, outfile)
                printw("Your game has been saved.\n")
        except IOError:
            printw("There was an error saving your game.")

        # change parsed_input to dummy text so no other commands will be executed
        parsed_input['command'] = 'pass'

    # load game
    elif parsed_input["command"] == 'loadgame':

        prompt = input("Are you sure you want to load your game (y/n)? ")
        if (prompt == 'Y') or (prompt=='y'):
            try:
                with open("saved_data.json") as file:
                    load_data = json.load(file)

            except FileNotFoundError:
                print("\nSave game data file could no be found.")

            # set player's location, inventory, locations visited, puzzles solved, and painting status
            player.set_location(load_data['current_location'])
            player.set_inventory(load_data['inventory'], game_rooms, game_items)
            player.set_locs_visited(load_data['locs_visited'])
            player.update_current_puzzle(load_data['cur_puzzle'])
            cur_puzzle = player.get_current_puzzle()
            player.update_painting_status(load_data['painting_status'])

            # clear location of all items
            for room in game_rooms.values():
                room.current_items = []

            # set each location's item in the game world
            for item in game_items:
                if load_data['item_locs'][item] != 'inventory':
                    game_items[item].set_current_loc(load_data['item_locs'][item])
                    game_rooms[load_data['item_locs'][item]].current_items.append(item)

            # give player items associated with any previously solved puzzles
            for i in range(cur_puzzle+1):
                # give puzzle item to player if there is one and if player currently doesn't have it
                if cur_puzzle > 1:
                    if (puzzle_items[cur_puzzle-1].get_item_given() != '') and (player.has_item(puzzle_items[cur_puzzle-1].get_item_given()) == False):
                        player.add_item(puzzle_items[cur_puzzle-1].get_item_given())
                    
            printw("\nYour game has been loaded successfully.")

            parsed_input['command'] = 'look'
            display_location(player.get_location())
            
        else:
            printw("\nOk, your game will not be loaded.")

    # ----------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------
    #
    # test for puzzle completion
    cur_puzzle = player.get_current_puzzle()
    # see if we are in the right position to solve the puzzle
    if player.get_location() == puzzle_items[cur_puzzle].get_puzzle_location():
        # we are in the right location to solve the puzzle
        # handle the safe opening puzzle
        if cur_puzzle == 4 and parsed_input['command'] == 'input code' and player.get_painting_status() == 1:
            if get_safe_input():
                # the puzzle has been solved
                # print out the solved description
                printw(puzzle_items[cur_puzzle].get_solved_description())
                print("")
                # give the player the item (keys)
                player.add_item(puzzle_items[cur_puzzle].get_item_given())
                printw(puzzle_items[cur_puzzle].get_item_given() + " has been added to your inventory.")
                # update the player's current puzzle
                player.update_current_puzzle(cur_puzzle+1)
                return
            else:
                printw("You try the code, but nothing happens.")
                return
        if puzzle_items[cur_puzzle].determine_solved(parsed_input['command'], parsed_input['item'], parsed_input['item2']):
            # the puzzle has been solved
            # print out the solved description
            printw(puzzle_items[cur_puzzle].get_solved_description())
            print("")
            # give the item to the player if the player gets an item from puzzle completion
            if puzzle_items[cur_puzzle].get_item_given() != '':
                player.add_item(puzzle_items[cur_puzzle].get_item_given())
                printw(puzzle_items[cur_puzzle].get_item_given() + " has been added to your inventory.")
            # update the player's current puzzle
            player.update_current_puzzle(cur_puzzle+1)
            return
    #
    #
    # ----------------------------------------------------------------------------------------------------------
    # ----------------------------------------------------------------------------------------------------------

    if parsed_input['command'] == "@":
        # then it is an item specific command that has already been executed
        return

    # if we receive an item command and two valid items
    if parsed_input['command'] in item_commands and parsed_input['item'] != '' and parsed_input['item2'] != '':
        print(f"You tried to use {parsed_input['item']} with {parsed_input['item2']} to no avail...")
        return
    elif parsed_input['command'] in item_commands and parsed_input['item'] != '':
        print(f"You tried to use {parsed_input['item']} but nothing happened...")
        return

    # print items in game and their location (for debugging)
    if parsed_input['command'] == 'items':
        for item in game_items:
            print(item + ', ' + game_items[item].current_loc)

#--------------------------------------------------------
    # look
    # if item is parsed and item is located in room or in inventory, display item description
    if parsed_input['command'] == 'look':
        if parsed_input['item']:
            if game_rooms[player.get_location()].has_item(parsed_input['item'], game_rooms, player) or player.has_item(
                    parsed_input['item']):
                if parsed_input['item'] in ascii_dict:
                    print(ascii_dict[parsed_input['item']])
                printw(game_items[parsed_input['item']].look_description)
            else:
                printw("You don't see that here.")
        # otherwise, display the description for the room
        else:
            # ----------------------------------------------------------------------------------------------------------
            # ----------------------------------------------------------------------------------------------------------
            #
            # check to see whether to give normal or 'solved' short description for music room and master bedroom
            if player.get_location() == 'master bedroom' and player.get_painting_status() == 1:
                printw("You reenter the bedroom. The place looks so much better without that stupid painting. Plus, you"
                       " can now see that there is a safe on the wall. The safe is a combination lock, with a 4 character"
                       " combination required to unlock. You wonder what is inside...")
                game_rooms[player.get_location()].display_items(game_rooms, game_items, player)
            elif player.get_location() == 'music room' and player.get_current_puzzle() > 3:
                printw("You reenter the music room to the sound of the repetitive tune playing over and over again. "
                       "AEFC AEFC AEFC. It's not the best song, but it gets the toes tapping. You find yourself humming along.")
                game_rooms[player.get_location()].display_items(game_rooms, game_items, player)
            else:
                printw(game_rooms[player.get_location()].short_desc)
                game_rooms[player.get_location()].display_items(game_rooms, game_items, player)
            #
            #
            # ----------------------------------------------------------------------------------------------------------
            # ----------------------------------------------------------------------------------------------------------

    # get an item
    elif parsed_input['command'] == 'get' or parsed_input['command'] == 'pick up' or parsed_input['command'] == 'take':
        # if the room has the item, add it to the player's inventory
        if (game_rooms[player.get_location()].has_item(parsed_input['item'], game_rooms, player)):
            # if item is in room and is holdable
            if (game_items[parsed_input['item']].holdable == True):
                printw("You pick up the " + parsed_input['item'] + ".")
                player.add_item(parsed_input['item'])
                # and remove it from the room
                game_rooms[player.get_location()].remove_items(game_rooms, parsed_input['item'], player)
                # and change its location
                game_items[parsed_input['item']].current_loc = "inventory"
            # if item is in room and is not holdable
            else:
                printw("You can't pick that up.")
        else:
            printw("I don't see that item here.")

    # drop an item
    elif parsed_input['command'] == 'drop' or parsed_input['command'] == 'put down':
        # if the player has the item in their inventory
        if (player.has_item(parsed_input['item'])):
            printw("You drop the " + parsed_input['item'] + ".")
            # remove from their inventory
            player.remove_item(parsed_input['item'])
            # and add to the room
            game_rooms[player.get_location()].add_items(game_rooms, parsed_input['item'], player)
            # and change its location
            game_items[parsed_input['item']].current_loc = player.get_location()
        else:
            printw("You don't have that item.")

    # display the player's inventory
    elif parsed_input['command'] == 'inventory':
        # if inventory is empty
        if not (player.view_inventory()):
            printw("You are not carrying anything.")
        else:
            print("You are carrying:\n")
            for item in player.view_inventory():
                printw(item)

    # check whether the room has specified directional exit
    elif parsed_input['direction'] != '':
        if has_direction_exit(parsed_input['direction'], game_rooms, player):
            # ----------------------------------------------------------------------------------------------------------
            # ----------------------------------------------------------------------------------------------------------
            #
            # lock room if the player has not solved the puzzle to enter said room
            if game_rooms[player.get_location()].exits[0][parsed_input['direction']][0] == "storage room" and \
                    player.get_current_puzzle() < 2:
                printw("You try to open the large metal door, but it won't budge. You'll have to figure out some way to "
                       "get it open. Maybe that coin slot is useful...")
                return
            if game_rooms[player.get_location()].exits[0][parsed_input['direction']][0] == "attic" and \
                    player.get_current_puzzle() < 3:
                printw("You jump as high as you can, but alas, you can't reach the hook on the trapdoor. If only you had"
                       " some sort of long stick with a hook on it...")
                return
            #
            #
            # ----------------------------------------------------------------------------------------------------------
            # ----------------------------------------------------------------------------------------------------------
            # if the exit has not been visited by the player yet, print long desc
            if (game_rooms[player.get_location()].exits[0][parsed_input['direction']][0]) not in player.get_locs_visited():
                display_location(game_rooms[game_rooms[player.get_location()].exits[0][parsed_input['direction']][0]].name)
                printw(game_rooms[game_rooms[player.get_location()].exits[0][parsed_input['direction']][0]].long_desc)
            else:
                display_location(game_rooms[game_rooms[player.get_location()].exits[0][parsed_input['direction']][0]].name)
                # ------------------------------------------------------------------------------------------------------
                # ------------------------------------------------------------------------------------------------------
                #
                # check to see whether to give normal or 'solved' short description for music room and master bedroom
                if game_rooms[game_rooms[player.get_location()].exits[0][parsed_input['direction']][0]].name == \
                    'music room' and player.get_current_puzzle() > 3:
                    printw("You reenter the music room to the sound of the repetitive tune playing over and over again. "
                       "AEFC AEFC AEFC. It's not the best song, but it gets the toes tapping. You find yourself humming along.")
                elif game_rooms[game_rooms[player.get_location()].exits[0][parsed_input['direction']][0]].name == \
                        'master bedroom' and player.get_painting_status() == 1:
                    printw(
                        "You reenter the bedroom. The place looks so much better without that stupid painting. Plus, you"
                        " can now see that there is a safe on the wall. The safe is a combination lock, with a 4 character"
                       " combination required to unlock. You wonder what is inside...")
                else:
                    printw(game_rooms[game_rooms[player.get_location()].exits[0][parsed_input['direction']][0]].short_desc)
                #
                #
                # ------------------------------------------------------------------------------------------------------
                # ------------------------------------------------------------------------------------------------------
            # update player's location
            player.update_location(game_rooms[player.get_location()].exits[0][parsed_input['direction']][0])
            # display items in room
            game_rooms[player.get_location()].display_items(game_rooms, game_items, player)
            # display the player's location
        else:
            printw("Confident in your choice, you walk headfirst into a wall.")

    # check whether the room has specified room exit
    elif parsed_input['room'] != '':
        # if the room is an exit to your current location, update location
        if has_room_exit(parsed_input['room'], game_rooms, player):
            # ----------------------------------------------------------------------------------------------------------
            # ----------------------------------------------------------------------------------------------------------
            #
            if (player.get_location() == 'hallway' or player.get_location() == 'kitchen') and parsed_input["direction"] != '':
                # lock room if the player has not solved the puzzle to enter said room
                if game_rooms[player.get_location()].exits[0][parsed_input['direction']][0] == "storage room" and \
                        player.get_current_puzzle() < 2:
                    printw(
                        "You try to open the large metal door, but it won't budge. You'll have to figure out some way to "
                        "get it open. Maybe that coin slot is useful...")
                    return
                if game_rooms[player.get_location()].exits[0][parsed_input['direction']][0] == "attic" and \
                        player.get_current_puzzle() < 3:
                    printw(
                        "You jump as high as you can, but alas, you can't reach the hook on the trapdoor. If only you had"
                        " some sort of long stick with a hook on it...")
                    return
            #
            #
            # ----------------------------------------------------------------------------------------------------------
            # ----------------------------------------------------------------------------------------------------------
            # if the room has not been visited by player, give long description
            if parsed_input['room'] not in player.get_locs_visited():
                display_location(game_rooms[parsed_input['room']].name)
                printw(game_rooms[parsed_input['room']].long_desc)
            else:
                # ------------------------------------------------------------------------------------------------------
                # ------------------------------------------------------------------------------------------------------
                #
                # check to see whether to give normal or 'solved' short description for music room and master bedroom
                if game_rooms[parsed_input['room']].name == 'music room' and player.get_current_puzzle() > 3:
                    printw("You reenter the music room to the sound of the repetitive tune playing over and over again. "
                       "AEFC AEFC AEFC. It's not the best song, but it gets the toes tapping. You find yourself humming along.")
                elif game_rooms[parsed_input['room']].name == 'master bedroom' and player.get_painting_status() == 1:
                    printw("You reenter the bedroom. The place looks so much better without that stupid painting. Plus, you"
                        " can now see that there is a safe on the wall. The safe is a combination lock, with a 4 character"
                       " combination required to unlock. You wonder what is inside...")
                else:
                    printw(game_rooms[parsed_input['room']].short_desc)
                #
                #
                # ------------------------------------------------------------------------------------------------------
                # ------------------------------------------------------------------------------------------------------
            player.update_location(parsed_input['room'])
            # display items in room
            game_rooms[player.get_location()].display_items(game_rooms, game_items, player)
        elif player.get_location() == parsed_input['room']:
            print("Uhh... you're already in the " + parsed_input['room'] + "...")
        else:
            print("You try to enter the " + parsed_input['room'] +
                  " despite the fact that " + str(player.get_location()) +
                  " doesn't have a door leading there.")

    # if we get all of the way down here, they tried to go somewhere that was unrecignized
    elif parsed_input["command"] == 'go' or parsed_input["command"] == 'enter':
        print("You can't go there.")

    elif parsed_input["command"] == 'pass':
        pass

    # no valid inputs entered
    else:
        generate_random_phrase()
