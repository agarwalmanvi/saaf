import numpy as np
import random
import copy

class Structure:
	def __init__(self, var=10, density=0.8, epsilon=0.01):
		self.var = var
		self.votes = list(zip([0]*self.var,[0]*self.var)) # votes on arguments, type list
		self.density = density
		self.epsilon = epsilon
		#move self.iterations to saf and esaf functions
		self.initial_values = [0]*self.var # change randomInit for this
		self.attack_relations = np.zeros((self.var,self.var)) # zero matrix with appropriate size
		#removed self.votes_relations - put in a seperate structure

	def addArg(self):
		self.var = self.var + 1
		self.attack_relations = np.concatenate((self.attack_relations,np.zeros((1,self.var))), axis=0)
		self.attack_relations = np.concatenate((self.attack_relations,np.zeros((1,self.worldsNum+1)).T), axis=1)
		self.votes.append((0,0))

	def addArgs(self, n):
		for i in range(n):
				self.addArg()

	def deleteArg(self, num):
		if num <= self.var:
			self.var = self.var - 1 
			self.attack_relations = np.delete(self.attack_relations, (num), axis=0)
			self.attack_relations = np.delete(self.attack_relations, (num), axis=1)
			del self.votes[num]

	def attack(self,u, v):
		if u <= self.var and v <= self.var:
				self.attack_relations[u][v] = 1

	addVotes(self, argument, pro, con):
		self.votes[argument] = (pro,con)

	def addProVotes(self, argument, num):
		self.votes[argument] = (num,self.votes[argument][1])

	def addConVotes(self, argument, num):
		self.votes[argument] = (self.votes[argument][0], num)

	def addInitialVal(self, argument, value):
		self.initial_values[argument] = value

	def randomInit(self):
		self.initial_values = [np.random.uniform(0, 1) for i in xrange(self.var)]
		n_edges = self.var * self.density
		for i in range(self.var):
			edges = np.random.randint(n_edges*8/10, n_edges*12/10)
			arr = range(1,self.var+1)
			arr = np.random.permutation(arr)
			pos_edges = arr[0:edges]
			for j in range(self.var):
				if j in pos_edges:
					self.attack_relations [i][j] = 1
			self.attack_relations[i][i] = 0
		# indices=list(np.transpose(np.nonzero(self.attack_relations)))
		# for i in range(len(indices)):
		# 	row, col = indices[i]
		# 	self.votes_relations[(row, col)] = (np.random.randint(0, 50), np.random.randint(0, 50))
		self.votes = list(zip(np.random.randint(0, 50, size=self.var), np.random.randint(0, 50, size=self.var)))

	def votes_eval(self, argument):
		return self.votes[argument][0]/(self.votes[argument][0] + self.votes[argument][1] + self.epsilon)

	# move to relevant part -- not needed here in basic structure
	# def votes_relations_eval(self, arg1, arg2):
	# 	votes = self.votes_relations[(arg1, arg2)]
	# 	return votes[0]/(votes[0] + votes[1] + self.epsilon)

def doSaf(s, iters=0):
		#Implements RunTillIterations
		if iters != 0:
	    save_iterations = np.zeros(shape = (iters+1,len(s.initial_values)))
	    save_iterations [0,:] = s.initial_values
	    i = 0
	    condition = 0
	    while (condition == 0 and i < iters+1):
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

	    if condition == 1:
	    		print("Converged!")
	    		print("Number of iterations required was: ", i)
	    else:
	    		print("Ran out of iterations!")
	    		print("Try running until convergence, or increasing the number of iterations.")
	  #Implements RunUntilConvergence
    else:
    	save_iterations = np.zeros(shape = (1,len(s.initial_values)))
    	save_iterations [0,:] = s.initial_values
    	i = 0
    	condition = 0
    	while (condition == 0 and i < 300):	#300 is maximum number of iterations
	        current_iter = copy.deepcopy(save_iterations[i,:])
	        i +=  1
	        for j in range(len(s.initial_values)):        
	            tau = s.votes_eval(j)
	            attacking_set = s.attack_relations[:,j]
	            attacking_pos = np.where(attacking_set)
	            temp1 = np.subtract(np.ones(s.var),current_iter)
	            temp2 = np.take(temp1,attacking_pos)
	            current_iter[j] = tau*np.prod(temp2)
	        save_iterations = np.concatenate((save_iterations,np.zeros((1,len(s.initial_values)))), axis=0)
	        save_iterations[i,:] = current_iter
	        diff1 = np.subtract(save_iterations[i-1,:],save_iterations[i,:])
	        condition = (diff1 < 0.0000000001).prod()
	        diff2 = np.sum(np.absolute(diff1))
	        print("Iteration number:  ", i, " Difference is ", diff2)

	    if condition == 1:
	    	print("Converged!")
	    	print("Number of iterations required was: ", i)
	    else:
	    	print("Ran out of iterations!")
	    	print("Try increasing the number of iterations.")


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
            
















