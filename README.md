# Social Abstract Argumentation Frameworks

## Installation

### Requirements
* Python 3
* Packages numpy, random, copy



## Exploring Multiple Solutions 

The implementation for this part can be found in the folder "Simple Cycles".

The test_with_uniform_initialization() method needs to be passed an argumentation graph, the votes for the arguments and the filenames 
where the results are stores. The test cases we can can be found at the end of the file "simple_cycles.py". 


## Exploring Convergence 

The implementation for this can be found in the folder "Tetsing Convergence".

Python implementation of 4 social abstract argumentation frameworks
* Social Abstract Argumentation Framework (SAF)
* Extended Social Abstract Argumentation Framework (ESAF)
* Bipolar Social Abstract Argumentation Framework (BSAF)
* Extended Bipolar Social Abstract Argumentation Framework (EBSAF)


## Usage

The frameworks which were implemented can be used as follows:
```
from saaf import *

s = Structure()
```
Default values for a structure are - 10 arguments, attack relation density of 0.8, support relation density of 0.6,  epsilon value of 0.01. You can also specify your own parameters, for example, as shown below, with 50 arguments, attack relation density of 0.5, support relation density of 0.6, epsilon value of 0.05.

```
s = Structure(var=50, density=0.5, support_density=0.6, epsilon=0.05)
```
Other examples of workings are given below.

```
# initialise a random structure
s = randomInit()

# specify your own structure
# increase number of arguments by 1
s.addArg()
# increase number of arguments by 4
s.addArgs(4)    
# delete argument number 3
s.deleteArg(3)  
# make argument 3 attack argument 4
s.attack(3,4)   
# make argument 4 support argument 5
s.support(4,5)  
# add 10 pro votes and 12 con votes to argument 3
s.addVotes(3,10,12)
```
You can also use `s.addProVotes(arg, pro)` or `s.addConVotes(arg, con)` to individually add pro or con votes to an argument.

```
# add an initial value of 0.75 to argument 3 
# this value is used for finding the valuation of the argument iteratively
s.addInitialVal(3,0.75) 
# add 12 pro votes and 45 con votes on the relation where 3 attacks 4
s.addVotesOnRel(3,4,12,45)  
# add 30 pro votes and 23 con votes on the relation where 4 supports 5
s.addVotesOnSupportRel(4,5,30,23) 
```
Once you make a Structure, you can pass it to different functions to see what the valuation of arguments is like. 

Currently, this implementation only supports printing if the solution exists, and if it does and it does in most cases, as far as our simulations suggest), printing the valuation of the arguments that the iterative formula arrives at. This does not alter the Structure itself, so you can reuse it.
```
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
