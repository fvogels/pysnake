class Action:
    def __init__(self, name):
        self.__name = name

    def __str__(self):
        return self.__name


LEFT = Action('left')
RIGHT = Action('right')
UP = Action('up')
DOWN = Action('down')
