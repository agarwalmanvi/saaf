import numpy as np
import random
import copy

def jacobian_inverse_4_cycle(arg_val, votes, permutation):
    # the standard order is [0,1,2,3]
    standard = np.array(range(0,len(permutation),1))

    # change the order of the argument valuations and the votes according to the standard order 
    arg_val[permutation] = arg_val[standard]
    votes[permutation] = votes[standard]

    # this is the jacobian for the standard labelling 1-2-3-4 (cyclic)
    jacobian = []
    jacobian.append([0, votes[0][0]*(arg_val[3]-1), 0, votes[0][0]*(arg_val[1]-1)])
    jacobian.append([votes[1][0]*(arg_val[2]-1), 0, votes[1][0]*(arg_val[0]-1), 0])
    jacobian.append([0, votes[2][0]*(arg_val[3]-1), 0, votes[2][0]*(arg_val[1]-1)])
    jacobian.append([votes[3][0]*(arg_val[2]-1), 0, votes[3][0]*(arg_val[0]-1), 0])
    jacobian = np.array(jacobian)
    # tansform the jacobian so as to the get the jacobian for the given permutation 
    jacobian[standard,:] = jacobian[permutation,:]
    jacobian[:, standard] = jacobian[:,permutation]
    
    # finds the inverse of the jacobian
    try:
        inv = np.linalg.inv(jacobian)
    except np.linalg.LinAlgError:
        return [-1]
    else:
        return inv

def jacobian_inverse_5_cycle(arg_val, votes, permutation):       
    # standard labelling 0-1-2-3-4 (cyclic)
    standard = np.array(range(0,len(permutation),1))
    arg_val[permutation] = arg_val[standard]
    votes[permutation] = votes[standard]

    # this is the jacobian for the standard labelling 1-2-3-4-5 (cyclic)
    jacobian = []
    jacobian.append([0, votes[0][0]*(arg_val[4]-1), 0, 0, votes[0][0]*(arg_val[1]-1)])
    jacobian.append([votes[1][0]*(arg_val[2]-1), 0, votes[1][0]*(arg_val[0]-1),0, 0])
    jacobian.append([0, votes[2][0]*(arg_val[3]-1), 0, votes[2][0]*(arg_val[1]-1), 0])
    jacobian.append([0, 0 , votes[3][0]*(arg_val[4]-1), 0, votes[3][0]*(arg_val[2]-1)])
    jacobian.append([votes[4][0]*(arg_val[3]-1), 0, 0, votes[4][0]*(arg_val[0]-1), 0])
    
    jacobian = np.array(jacobian)

    # tansform the jacobian so as to the get the jacobian for the given permutation 
    jacobian[standard,:] = jacobian[permutation,:]
    jacobian[:, standard] = jacobian[:,permutation]

    # finds the inverse of the jacobian
    try:
        inv = np.linalg.inv(jacobian)
    except np.linalg.LinAlgError:
        return [-1]
    else:
        return inv

    
def get_initial_set(increment, n_arg):
    # Uniformly seperates the space of [0,1]^n into (1/increment)^n equal sized blocks. Find a random configuration 
    # within those blocks. n_arg can only be 4,5
    initial_set = []
    l = np.arange(0,1,increment)
    for a in l:
        for b in l:
            for c in l:
                for d in l:
                    x1 = random.uniform(a,a+increment)
                    x2 = random.uniform(b,b+increment)
                    x3 = random.uniform(c,c+increment)
                    x4 = random.uniform(d,d+increment)
                    if (n_arg == 5):
                        for e in l:
                            x5 = random.uniform(e,e+increment)
                            initial_set.append([x1,x2,x3,x4,x5])
                    else:
                        initial_set.append([x1,x2,x3,x4])
    return initial_set 

def write_to_file(filename, labelling, converged_values):
# appends the results to a file 
    file = open(filename, 'a')
    file.write("Labelling is  " + str(labelling) + "\n")
    for i in converged_values:
        file.write("The fixed point : " + str(i[0]) + "\n")
        file.write("Initialization : " + str(i[1]) + "\n")
        file.write("Frequency : " + str(i[2]) + "\n")
    file.close()

