# wrappingpaper

A collection of Python decorators and utilities to abstract away common/tedious Python patterns.

#### Notes

This package is more about providing interesting abstractions and trying to flesh out the possibilities of Python code organization. I am in no way saying that using these functions will provide "good" code and I am in no way condoning their use for creating evil Python code ;).

Some of the functions in here may incentivize less understandable code, but that's okay. I want to give them space to exist and hopefully we can develop them further to where they will be more understandable and provide more intuitive and familiar abstractions.

This package is about experimentation and trying to create basic, interesting, natural feeling, and convenient abstractions while sidelining the scrutiny of Python purists, and potentially people with more sense (!!). I want this to try to push the limits of the language to see what other interesting constructs we can facilitate.

So, I guess the motto of this package is to develop freely, but use responsibly. <3

One other thing to note though, some of these don't play nice with linters 😢

#### Simple Example
```python
import wrappingpaper as wp

@wp.contextdecorator
def doing_something(a, b):
    print(a)
    yield
    print(b)

# por que no los dos?

# you can do this
with doing_something(4, 5):
    print(1)
# prints 4 1 5

# as well as this
@doing_something(4, 5)
def something():
    print(1)
something()
# prints 4 1 5

```

#### Includes
 - [helper modules](#helper-modules)
    - real implementations of faux imports, meant as case-studies for import mechanic classes provided.
 - [logging / error handling](#logging)
    - catch errors thrown in a function and redirect to logger
 - [context managers](#context-managers)
   - context managers that double as function wrappers
 - [object properties](#properties)
    - class and instance caching
    - dynamic property objects - give properties nested attributes and methods !!
 - [function signature helpers](#function-signature)
    - override and apply updates to function signatures
    - filter function arguments that are outside the function schema
    - partial that actually updates the wrapper
 - [import mechanics](#import-mechanics)
    - create faux modules and customize how modules are imported (I did some of the confusing bits for us thankfully)
 - [iterables](#iterables)
    - includes some basic iterable functions that I've pulled from other projects so I don't have to keep duplicating them everywhere
 - [misc](#misc)
    - stuff I just haven't sorted. ya know?
    - retry on exception
    - check circular references


## Install

```bash
pip install wrappingpaper
```

## Usage
```python
import wrappingpaper as wp
```

### Helper Modules

These are faux modules that utilize `wrappingpaper`'s [import mechanics](#import-mechanics) to alter modules that are imported from them.

#### lazyimport
This is a simple implementation of lazy importing using the defined import mechanics.

```python
from lazyimport import sklearn
import librosa # sklearn imports will be lazy
```

#### presets
This is a re-implimentation of [bmcfee/presets](https://github.com/bmcfee/presets) that includes the import mechanics, instead of having to wrap modules afterwards. I may add a PR to that package, but implementing it here was trivial for the time being and I didn't feel like it was important enough to push it thru the review process.

```python
from presets import librosa
librosa.update(sr=44100) # now functions will default to sr=44100
```

### Logging

**NOTE: I haven't put in the work to mock logging objects for testing so beware that in their current form they are untested and most likely have 1 or 2 bugs in there.**

I was working on a project that was full of error suppression and logging. There would be functions wrapped in try except blocks, logging calls, and a lot of redundancy in the scaffolding needed.

So I did work to factor that out and perform many of the common patterns in decorators.

The logging decorators here are primarily for functions that can be permitted to fail and return a default/empty value without the rest of the program breaking.

It also has utilities for pulling information from tracebacks. I haven't done anything about the logging Handlers and Formatters so that's a TODO.

```python
import logging
log = logging.getLogger(__name__)

# handle and log error

@wp.log_error_as_warning(log, default=dict)
def get_stats(x=None):
    if x is True:
        raise ValueError() # some error happens
    return {'a': 5, 'b': 6}

assert get_stats() == {'a': 5, 'b': 6}
assert get_stats(True) == {}
```

##### Roughly equivalent to:

```python
def get_stats(x=None):
    try:
        if x is True:
            raise ValueError() # some error happens
        return {'a': 5, 'b': 6}
    except ValueError as e:
        log.warning('Exception in get_stats: %s', e)
        return {}
```

### Context Managers

Two common patterns in Python are context managers and decorators. Often, they have the same basic structure: do some initialization, run a function, and do some cleanup.

And both can be useful in different contexts to give you clean code, but to use both, I often find myself writing an additional wrapper function around the context manager, and then you have to give it a slightly different name and it can get confusing.

So, in comes `contextdecorator` which works the same as `contextlib.contextmanager`, but it also doubles as a function decorator. When used as a decorator, it will call the function inside the context manager.

```python

@wp.contextdecorator
def doing_something(a, b):
    print(a)
    yield
    print(b)

# por que no los dos?

# you can do this
with doing_something(4, 5):
    print(1)

# as well as this
@doing_something(4, 5)
def something():
    print(1)
something()

```

Sometimes, your decorator isn't as simple and you need to do things a bit differently in the decorator (e.g. you need the name of the wrapped function).

```python

@doing_something.caller # override default decorator
def doing_something(func, a, b): # wrapped function, decorator arguments
    # change arguments
    name = func.__name__
    a = 'calling {}: {}'.format(name, a)
    b = 'calling {}: {}'.format(name, b)

    # return the wrapped function
    @functools.wraps(func)
    def inner(*args, **kw):
        with doing_something(a, b):
            return func(*args, **kw)
    return inner

```

##### Roughly equivalent to:

```python
import functools
from contextlib import contextmanager

@contextmanager
def doing_something(a, b):
    print(a)
    yield
    print(b)

def doing_something2(a, b):
    def outer(func):
        @functools.wraps(func)
        def inner(*a, **kw):
            with doing_something(a, b):
                return func(*a, **kw)
        return inner
    return outer

# used like:
with doing_something(4, 5):
    print(1)

@doing_something2(4, 5)
def something():
    print(1)
something()

```

### Properties

Python property objects are incredibly useful as they allow you to create natural feeling objects with some complex stuff all bundled up in a nice unsuspecting interface.

But using them, there are often times where I find myself writing the same classes stored many times over in utility files.

One use-case is caching. There are different levels of caching that you can provide.
 - `cachedproperty`: cached on the instance object - runs once per instance
 - `onceproperty`: cached on the class object - runs once per class/baseclass
 - `overridable_property`: works as a normal property (calls the wrapped function), until the property is assigned to. Then it returns the assigned value.
 - `overridable_method`: works as a normal method (calls the wrapped function), until the function is called as a decorator. Then it calls the wrapped function. Works on an instance level.

```python
import time

class SomeClass:
    @wp.cachedproperty
    def instance_prop(self):
        '''This is run once per object instance.'''
        return time.time()

    @wp.onceproperty
    def class_prop(self):
        '''This is run once. It is cached in the property
        object itself.'''
        return time.time()

    @wp.overridable_property
    def overridable(self):
        '''This property is run normally, until another value is assigned on top.'''
        return time.time()

    def __init__(self, overridable=None):
        if overridable: # override the property value
            # stores at self._overridable
            self.overridable = overridable
        # otherwise it just uses the property function like usual

a = SomeClass()
b = SomeClass()

assert a.instance_prop != b.instance_prop # prop runs once per object
assert a.class_prop == b.class_prop # prop runs only once
assert a.overridable != a.overridable # gets called twice, shouldn't be the same
a.overridable = 5
assert a.overridable == 5 # now the value is overridden

assert SomeClass(5).overridable == 5 # overriding inside class
```

### Function Signature

This is something that I'm looking for constantly.

Personally, I like the idea of config files that wrap up a bunch of function arguments into a file.

I also hate having to duplicate arguments when passing variables down 5 levels of nested function calls.

I like to just pass keyword arguments (`**kw`) down to the next function.

But there are cases, where there are extra config values in your keyword dict and you only want to pass the values that your function takes.


```python
# dynamic function defaults

@wp.configfunction
def asdf(a=5, b=6, c=7):
    return a + b + c

assert asdf() == 5+6+7 # normal behavior
asdf.update(a=1)
assert asdf() == 1+6+7 # updated default
assert asdf(3) == 3+6+7 # automatically resolves kwargs and posargs
asdf.clear()
assert asdf() == 5+6+7 # back to normal behavior

# filter out kwargs not in the signature (if **kw, it's a no-op).

@wp.filterkw
def asdf(a=5, b=6, c=7):
    return a + b + c

assert asdf(b=10, d=1234) == 5+10+7

```

### Objects


#### Monkeypatching
```python
class Blah:
    def asdf(self):
        return 10

b = Blah()

@wp.monkeypatch(b)
def asdf():
    return 11

assert asdf() == 11

asdf.reset() # remove patch
assert asdf() == 10

asdf.repatch() # re-place the patch
assert asdf() == 11
```

#### Namespace
```python
class something(metaclass=wp.namespace):
    one_thing = 5
    other_thing = 6

    def blah(x):
        return one_thing + other_thing + x

assert something.blah(10) == 5+6+10
```

### Iterables

```python
#####################
# loop breaking
#####################

items = wp.until(x if x != 7 else wp.done for x in range(10))
assert list(items) == list(range(0, 6))


####################
# loop throttling
####################

# make sure that a for loop doesn't go too fast.
# limit the time one iteration takes.
t0 = time.time()
for x in wp.throttled(range(10), 1):
    print(x)
assert time.time() - t0 > 10

# limiting the number of iterations to 10.
# with no iterable passed, it loops infinitely and
# yields the total yield time and the time it had to sleep.
for dt, time_asleep in wp.limit(wp.throttled(secs=1), 10):
    print('Iteration took {}s. Had to sleep for {}s.'.format(dt, time_asleep))
    print('-'*10)

################################
# Use `while True:` in a loop
################################

for _ in wp.infinite():
    print('this is gonna be a while...')


#########################
# pre-check an iterable
#########################

# check the first n items in an iterable, without removing them.

it = iter(range(6))
items, it = wp.pre_check_iter(it, 3)
assert items == [0, 1, 2]
assert list(it) == [0, 1, 2, 3, 4, 5, 6]


###########################################
# repeat and chain a function infinitely
###########################################

import random

def get_numbers(): # function returns an iterable
    return [random.random() for _ in range(10)]



numbers = wp.run_iter_forever(get_numbers)
# repeat get_numbers() and chain iterable outputs together
all_numbers = list(wp.limit(numbers, 100))
assert all(isinstance(x, float) for x in all_numbers)

# If no items are returned by a call, instead of the iterable hanging
# indefinitely waiting for an item, return None.

def get_numbers():
    if random.random() > 0.8: # make random breaks
        return # returns empty
    return [random.random() for _ in range(10)]

numbers = wp.run_iter_forever(get_numbers, none_if_empty=True)
# this SHOULD contain sporadic None's at a multiple of 10
all_numbers = list(wp.limit(numbers, 5000))
assert None in all_numbers

```

## Import Mechanics

This is probably the most dangerous thing to be playing with in here.

Python exposes a lot of its internal mechanics including its import system.

So we can take advantage of that to provide import wrappers that modify module behavior.

A basic example - lazy loading:

```python
# lazyimport/__init__.py
import wrappingpaper as wp
wp.lazy_loader.activate(__name__)


# main.py
from lazyimport import sklearn.model_selection

# sklearn is not currently loaded

sklearn.model_selection.train_test_split() # now it's loaded.
```

#### Modify a module after it has been imported from your pseudo-module
```python
import wrappingpaper as wp

@wp.PseudoImportFinder.modulemodifier
def my_loader(module):
    module.sneakything = '......hi'

my_loader.activate('somethingrandom')

# now somewhere else, you can do

from somethingrandom import numpy as np

assert np.sneakything == '......hi'
```
#### Wrap a module to modify the module's contents
```python
import importlib
import wrappingpaper as wp

# create the module wrapper that will traverse and modify the module when it is loaded.

class Module(wp.ModuleWrapper):
    # this is called for each item in the module
    def _wrapattr(self, attr, value):
        # do whatever you want with the value
        if callable(value) and getattr(value, '__doc__', None) is not None:
            value.__doc__ += '\nI was here.'
        elif self._is_submodule(value):
            value = Module(value)
        # always pass attr and modified value to be set,
        # otherwise it will be undefined.
        super()._wrapattr(attr, value)


# applies the module wrapper on load

@wp.PseudoImportFinder.moduleloader
def my_loader(spec):
    return Module(importlib.util.module_from_spec(spec))


# somewhere else (or in the same place. I'm not ur mom), actually use it

with my_loader.activated('somethingrandom'): # activated only inside context
    from somethingrandom import glob

print(glob.glob.__doc__)
assert glob.glob.__doc__.endswith('I was here.')
```


## Misc

Some other miscellaneous stuff that I have yet to organize.

```python
import random

# retry a function if an exception is raised

@wp.retry_on_failure(10)
def asdf():
    x = random.random()
    if x < 0.5:
        raise ValueError
    return x

# will either return a number that is definitely > 0.5
# or every number in the first 10 tries were below 0.5
try:
    assert asdf() > 0.5
except ValueError:
    print("Couldn't get a number :/")


# ignore error

with wp.ignore():
    a, b = 5, 0
    c = a / b # throws divide by zero
    a = 10 # never run
assert a == 5

```
