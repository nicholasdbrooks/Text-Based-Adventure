import textwrap as tr

class GameRoom:
    def __init__(self, name, short_desc, long_desc, init_items, current_items, exits) -> None:
        self.name = name
        self.short_desc = short_desc
        self.long_desc = long_desc
        self.init_items = init_items
        self.current_items = current_items
        self.exits = exits

    def printw(self, text) -> str:
    # @ params: text to print
    # @ return: none
    # prints text wrapped to a specified width
        print(tr.fill(text, width = 100))

    def has_item(self, item, game_rooms, player):
    # @ return: bool - True if room contains the item, false otherwise
        if item in self.current_items:
            return True
        else:
            return False

    def add_items(self, game_rooms, item, player):
        # adds an item to the room
        game_rooms[player.get_location()].current_items.append(item)

    def remove_items(self, game_rooms, item, player):
    # removes an item from the room
        if item in game_rooms[player.get_location()].current_items:
            game_rooms[player.get_location()].current_items.remove(item)
        else:
            print("That item is not located in this room.")

    def display_items(self, game_rooms, game_items, player):
        # prints the items currently located in the room
        for item in game_rooms[player.get_location()].current_items:
            # check to see if item exists in the game
            if (item in game_items):
                # and has a separate description to be displayed in the room
                if (game_items[item].room_description):
                    print("")
                    self.printw(game_items[item].room_description)