A simple library that implements a basic event system.

You can simply create classes, just use EventBase as second, or only base class, and use its methods.

Register event names in __init__ method using chain `self.initEvents(?delegateObject).registerNewEvents(*names: str)` 
```py
from SimpleEvents import *
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
```

Subscribe:
```py
ed = EventDict()

ed.subscribeToEvent("get", print)
ed.subscribeToEvent("set", print)
ed.subscribeToEvent("del", print)

```

Unsubscribe:
```py
ed = EventDict()

ed.unsubscribeToEvent("get", print)
ed.unsubscribeToEvent("set", print)
ed.unsubscribeToEvent("del", print)

```

In method notifySubscribersWithDataAuto, subscribers will be called with EventData object:
```
.args - list of ordered *args, passed to __init__()
.name - linked event name

Other:
The class is inherited from the word class, it has all the possibilities. But in addition, it can give access to data by key through the syntax of the attribute data.prop == data["prop"].

all unknown attributes will return None
data.unknown == None
```
