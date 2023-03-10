'''
Contains two classes from the "Observer Pattern".

These classes are:
- Observer
- Subject
'''

# Classes.
class Observer():
    '''
    Abstract class Observer from the "Observer Pattern".
    The system which observes the Subject implements this class further.
    '''
    def update(self, update_event):
        '''
        Update when something in the Subject happens.
        update_event specifies which part of the Observer should update.
        '''
        pass

class Subject():
    '''
    Class Subject from the "Observer Pattern".
    The system which is being observed by the Observer implements this class further.
    '''
    def __init__(self):

        self.observers = set()

    def attach(self, observer):
        '''
        Attaches an Observer, so this Observer can get updates when something happens.
        '''
        self.observers.add(observer)

    def notify(self, update_event, **kwargs):
        '''
        Notifiy all Observers about a change.
        update_event further specifies what exactly changed.
        *args for arguments that are important in combination with the change.
        '''
        for observer in self.observers:
            observer.update(update_event, **kwargs)
