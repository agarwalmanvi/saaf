# Social Abstract Argumentation Frameworks

Python implementation of 4 social abstract argumentation frameworks
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

# default values of 10 arguments, attack relation density of 0.8, support relation density of 0.6, 
# epsilon value of 0.01
s = Structure()
# you can also specify your own parameters -- 50 arguments, attack relation density of 0.5,
# support relation density of 0.6, epsilon value of 0.05
s = Structure(var=50, density=0.5, support_density=0.6, epsilon=0.05)
# initialise a random structure
s = randomInit()
# specify your own structure
s.addArg()      # increase number of arguments by 1
s.addArgs(4)    # increase number of arguments by 4
s.deleteArg(3)  # delete argument number 3
s.attack(3,4)   # make argument 3 attack argument 4
s.support(4,5)  # make argument 4 support argument 5
s.addVotes(3,10,12)      # add 10 pro votes and 12 con votes to argument 3
# you can also use s.addProVotes(arg, pro) or s.addConVotes(arg, con) to individually add pro or con votes to an argument
s.addInitialVal(3,0.75) # add an initial value of 0.75 to argument 3 
# this value is used for finding the valuation of the argument iteratively
s.addVotesOnRel(3,4,12,45)  # add 12 pro votes and 45 con votes on the relation where 3 attacks 4
s.addVotesOnSupportRel(4,5,30,23) # add 30 pro votes and 23 con votes on the relation where 4 supports 5

# once you make a Structure, you can pass it to different functions to see what the valuation of arguments is like. 
# Currently, this implementation only supports printing if the solution exists, and if it does 
# (and it does in most cases, as far as our simulations suggest), printing the valuation of the 
# arguments that the iterative formula arrives at. 
# This does not alter the Structure itself, so you can reuse it.
# Framework                                                   # Features
# Social Abstract Argumentation Framework                     # Votes on arguments, attack relations
doSaf(s)
# Extended Social Abstract Argumentation Framework            # SAF + votes on attack relations
doEsaf(s)
# Bipolar Social Abstract Argumentation Framework             # SAF + support relations
doBsaf(s)
# Extended Bipolar Social Abstract Argumentation Framework    # ESAF + support relations + votes on support relations
doEbsaf(s)
```

## Issues

