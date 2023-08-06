# Pytest Approxable Mixin
---
## Example
```python
from pytest_approxable import Approxable
from dataclasses import dataclass
from pytest import approx

@dataclass
class MetalProperties(Approxable):
    name: str
    heat_capacity: float
    conductivity: float

def test_metal_equal():
    mp1 = MetalProperties(name='metal1', heat_capacity=0.5, conductivity=1.)
    mp2 = MetalProperties(name='metal2', heat_capacity=0.499999999, conductivity=0.9999999998)
    assert approx(mp1.approxable_dict, abs=0.1) == mp2.approxable_dict

```
## Problem
When testing codes, we usually approximate floating numbers to avoid decimal points error. To do so, we use `pytest.approx` as follow
```python
from pytest import approx
def test_approx():
    a = 1.0000000000000001
    b = 1.
    assert approx(a, abs=0.1) == b # this will pass
    assert a == b # this will fail
```

Moreover, we can also use this with the dictionary derived from a dataclass. For example, 
```python
from dataclasses import dataclass, asdict
from pytest import approx

@dataclass
class MetalProperties:
    heat_capacity: float
    conductivity: float

def test_metal_equal():
    mp1 = MetalProperties(heat_capacity=0.5, conductivity=1.)
    mp2 = MetalProperties(heat_capacity=0.499999999, conductivity=0.9999999998)
    assert approx(asdict(mp1), abs=0.1) == asdict(mp2)
```
Now the problem arises when we have non-number fields in the class

```python
@dataclass
class MetalProperties:
    name: str
    heat_capacity: float
    conductivity: float

def test_metal_equal():
    mp1 = MetalProperties(name='metal1', heat_capacity=0.5, conductivity=1.)
    mp2 = MetalProperties(name='metal2', heat_capacity=0.499999999, conductivity=0.9999999998)
    assert approx(asdict(mp1), abs=0.1) == asdict(mp2)
```
Above code will fails since attribute `name` can't be approximated



##Progress

- [ ] tests
- [ ] supports nested object
