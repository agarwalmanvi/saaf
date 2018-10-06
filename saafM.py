import numpy as np
import random
import copy

class Structure:
	def __init__(self):
		self.var = 10
		self.votes = [] # votes on arguments, type list
		self.density = 0.8
		self.epsilon = 0.01
		self.iterations = 15
		self.initial_values = [] # will become numpy.ndarray when build
		self.attack_relations = np.zeros((self.var,self.var)) # zero matrix with appropriate size
		self.votes_relations = dict() # votes on relations - dict should be okay for sparse attack relations

	def build(self):
		self.initial_values = np.random.uniform(0,1,self.var) # NOT tau, only used for iterations
		n_edges = self.var * self.density
		#print(n_edges)
		for i in range(self.var):
			#print("For edge ", i)
			edges = np.random.randint(n_edges*8/10, n_edges*12/10)
			#print(n_edges*8/10)
			#print(n_edges*12/10)
			#print(edges)
			arr = range(1,self.var+1)
			#print(arr)
			arr = np.random.permutation(arr)
			#print(arr)
			pos_edges = arr[0:edges]
			#print(pos_edges)
			for j in range(self.var):
				if j in pos_edges:
					self.attack_relations [i][j] = 1
			self.attack_relations[i][i] = 0
			#print("-------------------------")
		#print(self.attack_relations)
		indices=list(np.transpose(np.nonzero(self.attack_relations)))
		for i in range(len(indices)):
			row, col = indices[i]
			self.votes_relations[(row, col)] = (np.random.randint(0, 50), np.random.randint(0, 50))
		self.votes = list(zip(np.random.randint(0, 50, size=self.var), np.random.randint(0, 50, size=self.var)))
		#print(self.votes)

	def votes_eval(self, argument):
		return self.votes[argument][0]/(self.votes[argument][0] + self.votes[argument][1] + self.epsilon)

	def votes_relations_eval(self, arg1, arg2):
		votes = self.votes_relations[(arg1, arg2)]
		return votes[0]/(votes[0] + votes[1] + self.epsilon)

def doSaf(s):
    save_iterations = np.zeros(shape = (s.iterations,len(s.initial_values)))
    save_iterations [0,:] = s.initial_values
    i = 0
    condition = 0
    while (condition == 0 or i < 3):
        current_iter = copy.deepcopy(save_iterations[i,:])
        i +=  1
        for j in range(len(s.initial_values)):        
            tau = s.votes_eval(j)
            attacking_set = s.attack_relations[:,j]
            attacking_pos = np.where(attacking_set)
            temp1 = np.subtract(np.ones(s.var),current_iter)
            temp2 = np.take(temp1,attacking_pos)
            current_iter[j] = tau*np.prod(temp2)
            
        save_iterations[i,:] = current_iter
        diff1 = np.subtract(save_iterations[i-1,:],save_iterations[i,:])
        condition = (diff1 < 0.0000000001).prod()
        diff2 = np.sum(np.absolute(diff1))
        print("Iteration number:  ", i, " Difference is ", diff2)

        print("Run till convergence")
        print("Number of iterations till convergence: ", i)
        #print("Fixed point obtained", save_iterations[i,:])

def doEsaf(s):
    # saves in every row the value after each iteration step
    save_iterations = np.zeros(shape = (s.iterations,len(s.initial_values)))
    save_iterations [0,:] = s.initial_values
    i = 0
    condition = 0
    while (condition == 0 or i < 3):
        current_iter = copy.deepcopy(save_iterations[i,:])
        i +=  1
        for j in range(len(s.initial_values)):        
            tau = s.votes_eval(j)
            attacking_set = s.attack_relations[:,j]
            attacking_pos = np.transpose(np.nonzero(attacking_set)).tolist()
            attacking_pos = [item for sublist in attacking_pos for item in sublist]
            temp1 = []
            for attacker in attacking_pos:
                if (attacker, j) in s.votes_relations:
                    tau_relations = s.votes_relations_eval(attacker, j)
                    temp1.append(1 - (tau_relations*current_iter[attacker]))
            current_iter[j] = np.prod(temp1)*tau
        save_iterations[i,:] = current_iter
        diff1 = np.subtract(save_iterations[i-1,:],save_iterations[i,:])
        condition = (diff1 < 0.0000000001).prod()
        diff2 = np.sum(np.absolute(diff1))
        print("Iteration number:  ", i, " Difference is ", diff2)

        print("Run till convergence")
        print("Number of iterations till convergence: ", i)
        #print("Fixed point obtained", save_iterations[i,:])
            
















