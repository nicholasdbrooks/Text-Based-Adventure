# Exceptions to handle errors - could be replaced by the 'return False' comments, but I kept the Exceptions in case
# we need to do more with error handling, etc
class ItemNotFound(Exception):
    pass


class ItemAlreadyHeld(Exception):
    pass


class LocationAlreadyVisited(Exception):
    pass


class Player:
    def __init__(self, cur_location, inventory=[], locs_visited=None, cur_puzzle=1, painting_status=0):

        # list - holds the players inventory
        # e.g. ['coin', 'piano_cartridge', 'fire_poker', ...]
        self.inventory = inventory

        # list - holds the locations that the player has visited (to track giving long/short desc)
        # e.g. ['Foyer', 'Office', 'Music Room', 'Library', ...]
        self.locs_visited = locs_visited

        # holds the players current location
        self.cur_location = cur_location
        # add the location to locs_visited
        self.add_location(cur_location)

        # holds the puzzle the player is currently working on
        self.current_puzzle = cur_puzzle

        # holds the status of the piano painting in the master bedroom (0 - on wall, 1 - taken down, safe exposed)
        self.painting_status = painting_status

    def update_painting_status(self, status):
        # updates the status of the piano painting in the master bedroom
        self.painting_status = status

    def get_painting_status(self):
        # returns the status of the piano painting in the master bedroom
        return self.painting_status

    def update_current_puzzle(self, puzzle):
        # updates the puzzle that the player is currently working on
        # there are 6 puzzles, do not iterate past the sixth puzzle
        if puzzle > 6:
            print("GAME OVER")
            exit()
        else:
            self.current_puzzle = puzzle

    def get_current_puzzle(self) -> int:
        # returns the puzzle that the player is currently working on
        return self.current_puzzle

    def add_item(self, item) -> bool:
        # adds an item to the player's inventory
        # check to see if inventory has been initialized
        if self.inventory is None:
            self.inventory = []

        # check to see if the item is already in the player's inventory
        if self.has_item(item):
            raise Exception(ItemAlreadyHeld)
            # return False

        # add the item to the player's inventory
        self.inventory.append(item)
        return True

    def remove_item(self, item) -> bool:
        # removes an item from the player's inventory
        # try to remove item from inventory
        if self.has_item(item):
            self.inventory.remove(item)
            return True
        else:
            # player does not have item in inventory
            raise Exception(ItemNotFound)
            # return False

    def view_inventory(self) -> list:
        # return the contents of the player's inventory
        return self.inventory

    def add_location(self, location) -> bool:
        # adds a location to the player's visited locations
        # check to see if locs_visited has been initialized
        if self.locs_visited is None:
            self.locs_visited = ["foyer"]
            return True

        # check to see if we have already added the location
        if location in self.locs_visited:
            raise Exception(LocationAlreadyVisited)
            # return False
        else:
            self.locs_visited.append(location)
            return True

    # def remove_location(self, location): is this needed? I can't think of any scenario where we'd remove a location

    def has_item(self, item) -> bool:
        # returns true if the player has a given item
        if not self.inventory:
            return False
        elif item in self.inventory:
            return True
        else:
            return False

    def get_location(self) -> str:
        # returns the player's current location
        return self.cur_location

    def set_location(self, loc) -> bool:
        # sets the player's current location
        self.cur_location = loc

    def get_locs_visited(self) -> list:
        # returns the locations the player has visited
        return self.locs_visited

    def set_locs_visited(self, locs):
        # sets the locations the player has visited
        self.locs_visited = locs

    def get_inventory(self) -> list:
        # returns the player's inventory
        return self.inventory

    def set_inventory(self, inv, game_rooms, game_items):
        # set player's inventory
        # remove any items in player's inventory from the corresponding room
        for item in inv:
            for room in game_rooms.values():
                if (item in room.current_items):
                    room.current_items.remove(item)
            game_items[item].set_current_loc('inventory')
        # override player's inventory with new list
        self.inventory = inv

    def update_location(self, location) -> None:
        # updates the player's current location
        self.cur_location = location

        # adds the location to the list of locations
        if location not in self.get_locs_visited():
            self.add_location(location)


if __name__ == "__main__":
    # test code
    p1 = Player("Foyer")

    # location functions
    print("Current Location: " + p1.get_location())
    p1.update_location("Library")
    print("Current Location: " + p1.get_location())
    print("Locations Visited: " + str(p1.get_locs_visited()) + "\n")

    # inventory functions
    p1.add_item("Fire Poker")
    p1.add_item("Coin")
    p1.add_item("Shovel")
    print("Current Inventory: " + str(p1.view_inventory()))
    print("Has Coin: " + str(p1.has_item("Coin")))
    p1.remove_item("Coin")
    print("Current Inventory: " + str(p1.view_inventory()))
    print("Has Coin: " + str(p1.has_item("Coin")))
