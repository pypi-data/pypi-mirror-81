# fancy-descriptors
This package add a callable descriptor called method descriptor which can apply on methods.

# Usage
### a simplest example:
```python

import fancy.descriptor as fd
class MyDescriptor(fd.MethodDescriptor):
    pass

class MyClass:
    @MyDescriptor
    def method_a(self):
        pass
    
    # or
    
    @MyDescriptor.bind()
    def method_b(self):
        pass

# after a MyClass object is created.
my_obj = MyClass()
assert isinstance(my_obj.method_a, MyDescriptor)

# returned {"method_a": <MyDescriptor object>, "method_b": <MyDescriptor object>}
MyDescriptor.get_marked_method(my_obj)
```

`the statement MyDescriptor.get_marked_method(my_obj) will get all marked methods' descriptors`

### with metadata
```python
import fancy.descriptor as fd

class MyDescriptor(fd.MethodDescriptor):
    def __init__(self,method, value: int, factory = None): 
        """
        method must at first place of argument
        factory is a method descriptor factory for underlying descriptor
        """
        super().__init__(method, factory)
        self._value = value

    def get_value(self):
        return self._value

class MyClass:
    # you cannot directly use MyDescriptor as decorator
    #  if the constructor of the descriptor has over one required argument
    # you must use .bind() to instead.
    @MyDescriptor.bind(value=1)
    def method_annotated(self):
        pass

my_obj = MyClass()

my_obj.method_annotated.get_value()  # returned 1
```

### Inheritance
```python

import fancy.descriptor as fd
class MyBaseDescriptor(fd.MethodDescriptor):
    pass

class MyDescriptor(MyBaseDescriptor):
    pass

class MyClass:
    @MyBaseDescriptor
    def method_base(self):
        pass

    @MyDescriptor
    def method_sub(self):
        pass

my_obj = MyClass()

MyBaseDescriptor.get_marked_method(my_obj)  # returned both method_base and method_sub
MyDescriptor.get_marked_method(my_obj)  # returned only method_sub
```