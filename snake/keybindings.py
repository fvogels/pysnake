class KeyBindings:
    def __init__(self):
        self.__table = {}

    def bind(self, key, buffer, action):
        self.__table[key] = (buffer, action)

    def process_key(self, key):
        if key in self.__table:
            buffer, action = self.__table[key]
            buffer.add(action)


class ActionBuffer:
    def __init__(self):
        self.__buffer = []

    def add(self, action):
        self.__buffer.append(action)

    def pop(self):
        if self.__buffer:
            result = self.__buffer[0]
            del self.__buffer[0]
            return result
        else:
            return None
