class Observer():

    def update(self, update_event):
        pass

class Subject():

    def __init__(self):
        self._observers = set()

    def attach(self, observer):
        self._observers.add(observer)

    def notify(self, update_event):
        for observer in self._observers:
            observer.update(update_event)