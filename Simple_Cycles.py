import numpy as np
import random
import copy
import util
import itertools


class Simple_Cycles():
    # the epsilon value we use 
    epsilon = 0.01
    # runs the iterative algorithm for this of iterations
    iterations = 2000
    # the threshold for the convergence limit = 10^-7
    convergence_threshold = 0.0000001
            
    def votes_evaluation(self, pro, con):
        return pro/(pro + con + self.epsilon)
        
    def test_with_uniform_initialization(self, attack_rel_init, votes_init, filename1, filename2):
        # the set of initial values we want to iterate to 
        initial_values_set = util.get_initial_set(0.2, len(votes_init))
        # the original permutation
        original_permutation = np.array(range(len(votes_init)))
        # finds all the possible permutations. This is used as different labellings 
        labellings = list(itertools.permutations(original_permutation))
        attack_rel = []
        votes = []
        for label in labellings:
            # stores the results for INR 
            # Of form [unique fixed points, initilizations, number of times it converges to that solution]
            inr_results = []
            # stores the results for ISS
            iss_results = []
            attack_rel = attack_rel_init
            label = np.array(label)
            # modify the attack_rel and the votes according to new labelling
            attack_rel[original_permutation,:] = attack_rel[label,:]
            attack_rel[:, original_permutation] = attack_rel[:,label]
            votes = votes_init
            votes[original_permutation] = votes[label]

            for i in range(len(initial_values_set)):
                #initial_values = np.array([ 0.4366013 ,  0.57195905,  0.16146849 , 0.8727271])

                # finds the converged values for 
                conv_INR = self.run_INR(initial_values_set[i], attack_rel, votes, label)
                conv_ISS = self.run_ISS(initial_values_set[i], attack_rel, votes, label)
                
                # the first value is directly appended
                if(i == 0):
                    inr_results.append([conv_INR, initial_values_set[i], 1])
                    iss_results.append([conv_ISS, initial_values_set[i], 1])
                else:
                    # for the others add depending if the fixe point has already been found
                    inr_results = self.add_to_existing(inr_results, conv_INR, initial_values_set[i])
                    iss_results = self.add_to_existing(iss_results, conv_ISS, initial_values_set[i])

            # Write the results for the labelling to the file
            util.write_to_file(filename1, label, inr_results)   
            util.write_to_file(filename2, label, iss_results)
    
    def add_to_existing(self, result, fixed_point, initialization):
        # result is of form [unique fixed points, initilization, frequency]
        for i in result:
            # the convergence threshold is decresed so has to not have multiple same fixed points 
            if (np.absolute(np.subtract(i[0], fixed_point)) < self.convergence_threshold*10).prod():
                i[2] = i[2] + 1
                return result
        result.append([fixed_point, initialization, 1])
        return result

    def run_ISS(self, initial_values, attack_relations, votes, labelling):
        # runs the ISS iterative algorithm
        save_iterations = np.zeros(shape = (self.iterations,len(votes)))
        save_iterations [0,:] = initial_values
        i = 0
        condition = 0
        while (condition == 0 and i < self.iterations-1):
            current_iter = copy.deepcopy(save_iterations[i,:])
            i +=  1
            for j in range(len(votes)):        
                # the iteration rule 
                tau = self.votes_evaluation(votes[j][0],votes[j][1])
                attacking_set = attack_relations[:,j]
                attacking_pos = np.where(attacking_set)
                temp1 = np.subtract(np.ones(len(votes)),current_iter)
                temp2 = np.take(temp1,attacking_pos)
                current_iter[j] = tau*np.prod(temp2)
            save_iterations[i,:] = current_iter
            # to store the total absolute change in value after every iteration
            diff1 = np.subtract(save_iterations[i-1,:],save_iterations[i,:])
            # the convergence condition, delta for each variable should be less than the convergence_threshold)
            condition = (np.absolute(diff1) < self.convergence_threshold).prod()
        if(i<self.iterations-1):
            return  save_iterations[i,:]
        else:
            return np.zeros(len(votes))

    def run_INR(self, initial_values, attack_relations, votes, labelling):
        # runs the INR iterative algorithm
        save_iterations = np.zeros(shape = (self.iterations,len(votes)))
        save_iterations [0,:] = initial_values
        i = 0
        condition = 0
        while (condition == 0 and i < self.iterations-1):
            # stores the value of the variables during the last iteration 
            current_iter = copy.deepcopy(save_iterations[i,:])
            # the current_iter_1 is used to store the function f, part of the iter rule
            current_iter_1 = copy.deepcopy(save_iterations[i,:])
            i +=  1
            for j in range(len(votes)):        
                # the iteration rule 
                tau = self.votes_evaluation(votes[j][0],votes[j][1])
                attacking_set = attack_relations[:,j]
                attacking_pos = np.where(attacking_set)
                temp1 = np.subtract(np.ones(len(votes)),current_iter)
                temp2 = np.take(temp1,attacking_pos)
                current_iter_1[j] = tau*np.prod(temp2)
            # 2nd part of iter rule 
            if(len(votes) == 4):
                part_2 = util.jacobian_inverse_4_cycle(current_iter, votes, labelling)
            else: 
                part_2 = util.jacobian_inverse_5_cycle(current_iter, votes, labelling)
            # if jacobian doesn't exist
            if (len(part_2) == 1):
                return np.zeros(len(votes))
            part_2 = np.dot(part_2, np.transpose(current_iter_1))

            save_iterations[i,:] = np.subtract(current_iter, part_2)
            # to store the total absolute change in value after every iteration
            diff1 = np.subtract(save_iterations[i-1,:],save_iterations[i,:])
            # the convergence condition, delta for each variable should be less than the convergence_threshold)
            condition = (np.absolute(diff1) < self.convergence_threshold).prod()
        if(i<self.iterations-1):
            return  save_iterations[i,:]
        else:
            return np.zeros(len(votes))
    
if __name__ == '__main__':
    # standard labelling 1-2-3-4 (cyclic)
    row1 = [0,1,0,1]
    row2 = [1,0,1,0]
    row3 = [0,1,0,1]
    row4 = [1,0,1,0]
    attack_rel = np.array([row1, row2, row3, row4])
    v = [1,0]
    # v2 = [2,0]
    votes = np.array([v2,v,v,v])

    # row1 = [0,1,0,0,1]
    # row2 = [1,0,1,0,0]
    # row3 = [0,1,0,1,0]
    # row4 = [0,0,1,0,1]
    # row5 = [1,0,0,1,0]
    # attack_rel = np.array([row1, row2, row3, row4, row5])
    # v = [1,0]
    # votes = np.array([v,v,v,v,v])

    # file which will contain the results for INR
    filename1 = 'INR_results.txt'

    # file which will contain the results for ISS
    filename2 = 'ISS_results.txt'
    Simple_Cycles().test_with_uniform_initialization(attack_rel, votes, filename1, filename2)

