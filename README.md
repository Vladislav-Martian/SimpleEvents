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
        super(EventDict, self).__init__(*args, **kwargs)
    
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


## Structure
- SimpleEvents
    - [-CLASS-] DelegateUnary
    - [-CLASS-] DelegateTuple
    - [-CLASS-] DelegateList      (Recomended, default)
    - [-CLASS-] EventData
    - [-CLASS-] EventBase
    - [-FUNCTION-] Dispatcher (works as decorator)

### Delegates:
In fact, they are containers of multiple functions and allow you to call them all, returning the last result. An unary delegate can only contain one function and will throw a TypeError when you try to merge it by .merge(otherDelegate).

You can easily create and apply your own delegate types (the default is DelegateList). You only need to implement a number of methods:
- invoke(*args, **kwargs) - invokes delegate
- add(func) - add function to delegate
- clear() - clear delegate
- remove() - remove first appearance of function indelegate
- merge() - merge delegate with other on-place [optional]

How to use custom delegates - goto EventBase description

## EventData
A simple dictionary-inherited container for storing event data. There are minor differences from the usual dictionary:
- `.args` - can contain an array of ordered elements with no keys passed to the constructor
- `.name` - is the name of the calling event
- Constructor signature is:
 `def __init__(self, name:str, *args , **kwargs)`
 ```py
 #you just can pass key-value pairs
 x = EventData(somekey="somevalue", somekey2=2)
 ```
- You can get key values not only through the [] operator, but also through accessing the attributes '.'. All unknown attributes will return None, but this works purely as a getter
```py
data.somekey == data["somekey"] == "somevalue"
data.unknown == None

data.unknown = "newvalue" # raises error, no setter
```
## EventBase
The basic interface for implementing an event system for an object.Just use it instead of 'object' when inheriting a new class, or if your class is already inheriting from another class, then as a second ancestor. Above is a primitive example of an event wrapper class for a dictionary.
Methods included in this class:
- `initEvents()` - must be called when the instance is created
- `registerNewEvent(name:str, *, delegateObject = None)` Registers a new event for an object. You can explicitly pass a custom delegate object for a given event `registerNewEvent(...delegateObject=MyDelegate())`
- `registerNewEvents(*names: str, delegateObjectType=None)` Registers multiple new events. You can also specify a custom delegate, but already in the form of the delegate class itself.
`registerNewEvents(...delegateObjectType=MyDelegate)`
- `subscribeToEvent(name: str, function: Callable` Subscribes the passed function to a specific event on the object, by its name.
`.subscribeToEvent("myEvent", lambda data: print(data))`
- `unsubscribeToEvent(name: str, function: Callable` reverses the result of the previous method
- `clearSubscribersAndRegistrations()` completely removes all registrations and subscribers
- `clearSubscribers()` removes all subscribers but leaves registrations
- `notifySubscribers(name: str, *args, **kwargs)` The simplest type of notification. All subscribers will be called with the given arguments.
- `notifySubscribersWithData(data: EventData)` works with a ready-made data object. The "sender" key automatically sets to a link to the caller.
- `notifySubscribersWithDataAuto(name: str, *args, **kwargs)` Completely repeats the previous method, but creates a data object on its own.

All of these methods, with the exception of three Notify methods, return the object they were called on. This allows you to build them as chains if it necessary to you.

Custom delegates are passed when registering events.

## Dispatcher
A primitive event system attached to a specific function. Works like a decorator.
```py
from SimpleEvents import Dispatcher

# don't forget about those parentheses.
# It is a parameterized decorator,
# with just one optional parameter.
# @Dispatcher(delegateObject = None)
@Dispatcher()
def doNothing():
    pass

@doNothing.subscribe
def noname():
    print("A")


@doNothing.subscribe
def noname():
    print("B")

doNothing.subscribe(noname) # after subscribing returns noname function, decorator-safe
doNothing.unsubscribe(noname) # after unsubscribing returns noname function, decorator-safe

doNothing()
# out:
# A
# B
```