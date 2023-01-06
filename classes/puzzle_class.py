class Puzzle:
    def __init__(self, num, puzzle_location, key_item, key_command, key_item2, solved_description, item_given):
        self.puzzle_num = num
        self.puzzle_location = puzzle_location
        self.key_item = key_item
        self.key_command = key_command
        self.key_item2 = key_item2
        self.solved_description = solved_description
        self.item_given = item_given

    def determine_solved(self, command, item, item2) -> bool:
        # determines whether the puzzle has been solved
        # @params: command, item, use_on that were input by the player
        # i.e. put nickel in coin slot: command = put, item = nickel, use_on = coin slot
        # @return: returns true if this input solves the puzzle, false otherwise
        if command in self.key_command and item in self.key_item and item2 in self.key_item2:
            return True
        return False

    def get_solved_description(self) -> str:
        # returns a string of the description when the puzzle has been solved
        return self.solved_description

    def get_puzzle_location(self) -> str:
        # returns a string of the room the player must be in to solve the puzzle
        return self.puzzle_location

    def get_item_given(self) -> str:
        # returns the item that will be given to the player upon completion of the puzzle
        return self.item_given
