class Timer:
    def __init__(self, delay):
        self.__delay = delay
        self.__elapsed_seconds = 0

    def tick(self, elapsed_seconds):
        self.__elapsed_seconds += elapsed_seconds

    @property
    def ready(self):
        return self.__elapsed_seconds >= self.__delay

    def consume(self):
        if not self.ready:
            raise RuntimeError()
        self.__elapsed_seconds -= self.__delay
