# Formulator

Formulator validates properties of python objects with standard field validation and typing abstractions.
Formulator can be written in declarative style or embedded into existing code via annotations.

Basic Usage
-----------

### Method 1 - pluggable into any existing code: annotations via decorators

```python
from formulator import *

@typeCheck
def floatAdd(arg1: NegativeInteger, arg2: Negative) -> Float:
    return arg1 + arg2 + 0.5
```

- <span style="color:coral;">Used in this way, Formulator guarantees that the code will execute per the original writing.</span>
- <span style="color:coral;">If there is a typing error, the code will print to the console (or log, if logging is enabled) any errors that the type checker encounters.</span>
- <span style="color:cyan;">Don't want the validation active? Simply remove the decorator from the code.</span>

### Method 2 - Subclass the minimal overhead Node provided by Formulator and use declaratively

```python
from formulator import *

class MyObject(Node):
    identifier = Integer()
    name = SizedRegexString()
    description = String()
    coordinates = PreciseFloat()
```

- <span style="color:coral;">Instantiations of MyObject will require {identifier, name, description, and coordinates} as arguments in that order (or via keywords).</span>
- <span style="color:coral;">Instantiations with arguments that do not meet the requirement will throw a FieldValidationError- and so heavily imposes the typing restriction.</span>

Documentation
-------------
A GitBook link is currently being constructed.

Feedback
--------
Formulator remains a one-off pluggable utility library. The idea is that the decorator can be added ex-post to any python code annotated with the Formulator Descriptors.
All support tickets welcome.

Contrib
-------

Pluggable expansions for this general validator framework are planned for the future
If you want to work on the project, please <a href="mailto:trijeets@gmail.com">mail me</a>