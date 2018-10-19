# Social Abstract Argumentation Frameworks

Command-line implementation of 4 social abstract argumentation frameworks
* Social Abstract Argumentation Framework (SAF)
* Extended Social Abstract Argumentation Framework (ESAF)
* Bipolar Social Abstract Argumentation Framework (BSAF)
* Extended Bipolar Social Abstract Argumentation Framework (EBSAF)

## Installation

### Requirements
* Python 3
* Packages numpy, random, copy

## Usage

```
from saaf import *

# default values of 10 arguments, attack relation density of 0.8, support relation density of 0.6, epsilon value of 0.01
s = Structure()
# you can also specify your own parameters -- 50 arguments, attack relation density of 0.5, support relation density of 0.6, epsilon value of 0.05
s = Structure(var=50, density=0.5, support_density=0.6, epsilon=0.05)
```

## Issues
