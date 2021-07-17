import unittest
from unittest.main import main
from SimpleEvents import *

# Even-system frame to dict
class EventDict(dict, EventBase):
    def __init__(self, *args, **kwargs):
        self.initEvents().registerNewEvents(
            "get", "set", "del"
        )
        super(EventDict, self).__init__()
    
    def get(self, key, *args, **kwargs):
        self.notifySubscribersWithDataAuto("get", key=key)
        return super(EventDict, self).get(key, *args, **kwargs)
    
    def __getitem__(self, key, *args, **kwargs):
        self.notifySubscribersWithDataAuto("get", key=key)
        return super(EventDict, self).__getitem__(key, *args, **kwargs)
    
    def __setitem__(self, key, *args, **kwargs):
        self.notifySubscribersWithDataAuto("set", key=key)
        return super(EventDict, self).__setitem__(key, *args, **kwargs)
    
    def __delitem__(self, key, *args, **kwargs):
        self.notifySubscribersWithDataAuto("del", key=key)
        return super(EventDict, self).__delitem__(key, *args, **kwargs)



class TestEventClass(unittest.TestCase):

    def testDictionary(self):
        ed = EventDict()

        ed.subscribeToEvent("get", self.assertTrue)
        ed.subscribeToEvent("set", self.assertTrue)
        ed.subscribeToEvent("del", self.assertTrue)
        ed.subscribeToEvent("get", print)
        ed.subscribeToEvent("set", print)
        ed.subscribeToEvent("del", print)

        ed[4] = 4
        x = ed[4]
        ed[6] = 6
        del ed[4]

        
    
    def testDispatcherSubscribe(self):
        @Dispatcher()
        def disp():
            pass
        
        @disp.subscribe
        def handler():
            print("Handler Call")
            self.assertTrue(True)
        
        disp()
    
    def testDispatcherUnsubscribe(self):
        @Dispatcher()
        def disp():
            pass

        @disp.subscribe
        def handler():
            print("Handler Call")
            self.fail
        
        disp.unsubscribe(handler)

        self.assertTrue(True)

        disp()


class TestDelegates(unittest.TestCase):
    def testAllInOne(self):
        delegate = DelegateList()
        delegate2 = DelegateList()


        delegate + print
        delegate - print

        delegate2 + print
        delegate2 + print

        delegate.merge(delegate2)

        delegate("Teststring")


if __name__ == '__main__':
    unittest.main()
