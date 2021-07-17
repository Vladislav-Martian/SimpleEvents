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


# after subscribing returns noname function, decorator-safe
doNothing.subscribe(noname)
# after unsubscribing returns noname function, decorator-safe
doNothing.unsubscribe(noname)

doNothing()
