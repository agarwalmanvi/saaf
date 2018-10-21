
import numpy as np
import random
import copy

class simple_SAAF():
    # epsilon thats used for vote aggregation
    epsilon = 0.1
     # runs the iterative algorithm for given number of iterations
    iterations = 10000
    # number of arguments and the density of the frame 
    var = 5
    density = 0.8

    # take care of zeros 
    def votes_evaluation(self, pro, con):
        return pro/(pro + con + self.epsilon)
    
    def run_till_convergence(self, initial_values, attack_relations, votes):
        
        # saves in every row the value after each iteration step
        save_iterations = np.zeros(shape = (self.iterations,len(initial_values)))
        save_iterations [0,:] = initial_values
        i = 0
        condition = 0
        while (condition == 0 and i < self.iterations-1):
            current_iter = copy.deepcopy(save_iterations[i,:])
            i +=  1
            for j in range(len(initial_values)):        
                # the iteration rule 
                tau = self.votes_evaluation(votes[j][0],votes[j][1])
                attacking_set = attack_relations[:,j]
                attacking_pos = np.where(attacking_set)
                temp1 = np.subtract(np.ones(self.var),current_iter)
                temp2 = np.take(temp1,attacking_pos)
                current_iter[j] = tau*np.prod(temp2)
            save_iterations[i,:] = current_iter
            # to store the total absolute change in value after every iteration
            diff1 = np.subtract(save_iterations[i-1,:],save_iterations[i,:])
            # the convergence condition, delta for each variable should be less than 10^-10
            condition = (np.absolute(diff1) < 0.0000001).prod()
            diff2 = np.sum(np.absolute(diff1))
            #print("Iteration number:  ", i, " Difference is", diff2)
            #print("Fixed point obtained", save_iterations[i,:])
        if(i<self.iterations-1):
            return  save_iterations[i,:]
        else:
            return [0,0,0,0,0]
        # print("Run till convergence")
        # print("Number of iterations till convergence", i)
        # print("The values after ith iteration", save_iterations[i,:])

    def main(self):
        # initial value of the variables is randomly set to a value in [0,1)
        initial_values = np.random.uniform(0,1,self.var)
        n_edges = self.var * self.density 
        # the attack relations matrix. if [i][j] = 1 then i attacks j
        attack_relations = np.zeros(shape = (self.var,self.var))
        for i in range(self.var):
             # the number of edges for each argument is samples from, density +- 10%
             edges = np.random.randint(n_edges*8/10, n_edges*12/10)
             # permutation of the edges
             arr = range(1,self.var+1)
             arr = np.random.permutation(arr)
             # these are the arguments that i_th argument  attacks
             pos_edges = arr[0:edges]
             for j in range(self.var):
                if j in pos_edges:
                    attack_relations [i][j] = 1
             # removes all the self attacks         
             attack_relations[i][i] = 0

        # initalize the votes given to the arguments. The votes are ranomly intilised from 0 to 500. Better way needed !
        votes = np.random.randint(0,50, (self.var,2))
        #print("Initial values", initial_values)
        self.run_for_iterations(initial_values, attack_relations, votes)
        # print("Initial values", initial_values)
        self.run_till_convergence(initial_values, attack_relations, votes)

    def test(self):

        # standard labelling 1-2-3-4-5 (cyclic)
        row1 = [0,1,0,0,1]
        row2 = [1,0,1,0,0]
        row3 = [0,1,0,1,0]
        row4 = [0,0,1,0,1]
        row5 = [1,0,0,1,0]
        attack_rel = np.array([row1, row2, row3, row4, row5])
        v = [1,0]
        votes = np.array([v,v,v,v,v])

        # # standard labelling 1-2-3-4 (cyclic)
        # row1 = [0,1,0,1]
        # row2 = [1,0,1,0]
        # row3 = [0,1,0,1]
        # row4 = [1,0,1,0]
        # attack_rel = np.array([row1, row2, row3, row4])
        # v = [1,0]
        # v1 = [2,0]
        # votes = np.array([v1,v,v,v])

        # specify permutation of the labellings
        permutation = [1,3,2,4,5]

        # Specify the permutation 
        permutation = [x - 1 for x in permutation]        
        standard = range(0,len(permutation),1)
        attack_rel[standard,:] = attack_rel[permutation,:]
        attack_rel[:, standard] = attack_rel[:,permutation]

        ini_val = np.array([None]*50)
        conv = np.array([None]*50)
        j = 0
        for i in range(50):
            print(i)
            found = False
            # initial_values = np.random.uniform(0,1,4)
            initial_values = np.array([ 0.1386 ,  0.78308,  0.08145 , 0.58693, 0.2971])

            converged_values = self.run_till_convergence(initial_values, attack_rel, votes)
            for k in range(j):
                if (np.absolute(np.subtract(conv[k],converged_values))<0.000001).prod():
                    found = True
            if (found == False):
                conv[j] = converged_values
                ini_val[j] = initial_values
                j += 1
        for i in range(j):
            print("Initial Value", ini_val[i])
            print("Converged Value", conv[i])
        
        # [ 0.4366013   0.57195905  0.16146849  0.8727271 ] - model 2 - with label(1-2-3-4)
        # [ 0.36578813  0.04296254  0.61881948  0.37567131] - model 3 - with label(1-2-3-4)

# [ 0.36572807  0.36572807  0.36572807  0.36572807] - model 1
# [ 0.01125178  0.88874822  0.01125178  0.88874822] - model 2 
# [ 0.88874822  0.01125178  0.88874822  0.01125178] - model 3 


if __name__ == '__main__':
    # simple_SAAF().main()
    simple_SAAF().test()

    