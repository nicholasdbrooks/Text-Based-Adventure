class GameItem:
    def __init__(self, name, room_description, starting_loc, current_loc, look_description, holdable, synonyms, verbs, isGameKey, isStoryItem, relatedItems) -> None:
        self.name = name
        self.room_description = room_description
        self.starting_loc = starting_loc
        self.current_loc = current_loc
        self.look_description = look_description
        self.synonyms = synonyms
        self.holdable = holdable
        self.verbs = verbs
        self.isGameKey = isGameKey
        self.isStoryItem = isStoryItem
        self.relatedItems = relatedItems

    def set_current_loc(self, room):
        self.current_loc = room