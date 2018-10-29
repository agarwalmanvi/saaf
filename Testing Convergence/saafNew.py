import numpy as np
import random
import copy
import scipy
from scipy import special
import time
import math
from scipy.sparse import rand

class Structure:
	def __init__(self, var=10, density=0.8, support_density=0.6, epsilon=0.01):
		self.var = var
		self.votes = list(zip([0]*self.var,[0]*self.var)) 
		self.density = density
		self.epsilon = epsilon
		self.initial_values = [0]*self.var
		self.attack_relations = np.zeros((self.var,self.var)) # zero matrix with appropriate size
		self.votes_relations = dict()
		self.support_density = support_density
		self.support_relations = np.zeros((self.var,self.var)) # zero matrix with appropriate size
		self.votes_support_relations = dict()

		self.results = 0
		self.time = 0
		self.iterations_needed = 0


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

	def support(self, u,v):
		if u <= self.var and v <= self.var:
			self.support_relations[u][v] = 1

	def addVotes(self, argument, pro, con):
		self.votes[argument] = (pro,con)

	def addProVotes(self, argument, num):
		self.votes[argument] = (num,self.votes[argument][1])

	def addConVotes(self, argument, num):
		self.votes[argument] = (self.votes[argument][0], num)

	def addInitialVal(self, argument, value):
		self.initial_values[argument] = value

	def addVotesOnRel(self,arg1,arg2,pro,con):
		self.votes_relations[(arg1,arg2)] = (pro,con)
	
	def addVotesOnSupportRel(self, arg1, arg2, pro, con):
		self.votes_support_relations[(arg1,arg2)] = (pro,con)
		
	def randomInit(self):
		# random values between 0 and 1 for each argument to use in the iterations
		self.initial_values = [np.random.uniform(0, 1) for i in range(self.var)]
		# total number of edges needed to get desired density
		n_edges = math.floor(2 * scipy.special.comb(self.var, 2) * self.density)
		# keeps track of which nodes still have space for more edges
		available_nodes = list(range(self.var))
		# the attacking relations are added here
		for i in range(n_edges):
			u = np.random.choice(available_nodes)
			# ensures that u does not end up in free_nodes
			self.attack_relations[u][u] = 1
			conn_nodes = self.attack_relations[u]
			# nodes that are available to be connected
			free_nodes = np.where(conn_nodes == 0)
			# if no nodes are available, remove u from available nodes
			if free_nodes[0].size == 0:
				available_nodes.remove(u)
				i -= 1
			# if free nodes are available, set value in attack relation adjacency matrix to 1
			else:
				v = np.random.choice(free_nodes[0])
				self.attack_relations[u][v] = 1
			# no self attacks
			self.attack_relations[u][u] = 0	
		n_edges = math.floor(2 * scipy.special.comb(self.var, 2) * self.support_density)
		available_nodes = list(range(self.var))
		# for support relations the same thing is done
		for i in range(n_edges):
			u = np.random.choice(available_nodes)
			self.support_relations[u][u] = 1
			conn_nodes = self.support_relations[u]
			free_nodes = np.where(conn_nodes == 0)
			if free_nodes[0].size == 0:
				available_nodes.remove(u)
				i -= 1
			else:
				v = np.random.choice(free_nodes[0])
				# checks so that there aren't both support and attack relations between two arguments 
				if self.attack_relations[u][v] == 0:
					self.support_relations[u][v] = 1
			self.support_relations[u][u] = 0	
		# votes on attack relations
		indices=list(np.transpose(np.nonzero(self.attack_relations)))
		for i in range(len(indices)):
			row, col = indices[i]
			self.votes_relations[(row, col)] = (np.random.randint(0, 50), np.random.randint(0, 50))
		# votes on arguments
		self.votes = list(zip(np.random.randint(0, 50, size=self.var), np.random.randint(0, 50, size=self.var)))
		# votes on support relations
		indices=list(np.transpose(np.nonzero(self.support_relations)))
		for i in range(len(indices)):
			row, col = indices[i]
			self.votes_support_relations[(row, col)] = (np.random.randint(0, 50), np.random.randint(0, 50))

	def votes_eval(self, argument):
		return self.votes[argument][0]/(self.votes[argument][0] + self.votes[argument][1] + self.epsilon)

	def votes_relations_eval(self, arg1, arg2):
		votes = self.votes_relations[(arg1, arg2)]
		return votes[0]/(votes[0] + votes[1] + self.epsilon)

	def votes_support_relations_eval(self, arg1, arg2):
		votes = self.votes_support_relations[(arg1, arg2)]
		return votes[0]/(votes[0] + votes[1] + self.epsilon)

def doSaf(s, iters=10000):
	# store time for runtime
	t0 = time.time()
	# initialise matrix for storing iteration values
	save_iterations = np.zeros(shape = (iters+1,len(s.initial_values)))
	# take the initial values for the 0th iteration
	save_iterations [0,:] = s.initial_values
	i = 0
	condition = 0
	# iterate until convergence as long as you dont run out of iterations
	while (condition == 0 and i < iters+1):
		current_iter = copy.deepcopy(save_iterations[i,:])
		i +=  1
		# iterative rule
		for j in range(len(s.initial_values)):        
			tau = s.votes_eval(j)
			attacking_set = s.attack_relations[:,j]
			attacking_pos = np.where(attacking_set)
			temp1 = np.subtract(np.ones(s.var),current_iter)
			temp2 = np.take(temp1,attacking_pos)
			current_iter[j] = tau*np.prod(temp2)
		# store values in iteration matrix
		save_iterations[i,:] = current_iter
		# compare with convergence threshold
		diff1 = np.subtract(save_iterations[i-1,:],save_iterations[i,:])
		condition = (np.absolute(diff1) < 0.0000000001).prod()
		diff2 = np.sum(np.absolute(diff1))
	if condition == 1:
		s.time = time.time() - t0
		s.iterations_needed = i
		s.results = str(1)
		print("Converged!")
	else:
		print("Ran out of iterations!")
		s.results = str(0)
		s.time = 0
		s.iterations_needed = 0
	
def doEsaf(s, iters=10000):
	t0 = time.time()
	save_iterations = np.zeros(shape = (iters+1,len(s.initial_values)))
	save_iterations [0,:] = s.initial_values
	i = 0
	condition = 0
	while (condition == 0 and i < iters+1):
		current_iter = copy.deepcopy(save_iterations[i,:])
		i +=  1
		for j in range(len(s.initial_values)):    
			# the iterative rule    
			tau = s.votes_eval(j)
			attacking_set = s.attack_relations[:,j]
			attacking_pos = np.transpose(np.nonzero(attacking_set)).tolist()
			attacking_pos = [item for sublist in attacking_pos for item in sublist]
			temp1 = []
			# the votes of the attack relations are included for all the attackers 
			for attacker in attacking_pos:
				if (attacker, j) in s.votes_relations:
					tau_relations = s.votes_relations_eval(attacker, j)
					temp1.append(1 - (tau_relations*current_iter[attacker]))
			current_iter[j] = np.prod(temp1)*tau
		save_iterations[i,:] = current_iter
		diff1 = np.subtract(save_iterations[i-1,:],save_iterations[i,:])
		condition = (np.absolute(diff1) < 0.0000000001).prod()
		diff2 = np.sum(np.absolute(diff1))

	if condition == 1:
		print("Converged!")
		s.time = time.time() - t0
		s.iterations_needed = i
		s.results = str(1)
	else:
		print("Ran out of iterations!")
		s.time = 0
		s.iterations_needed = 0
		s.results = str(0)

def doBsaf(s, iters=10000):
	t0 = time.time()
	save_iterations = np.zeros(shape = (iters+1,len(s.initial_values)))
	save_iterations [0,:] = s.initial_values
	i = 0
	condition = 0
	while (condition == 0 and i < iters+1):
		current_iter = copy.deepcopy(save_iterations[i,:])
		i +=  1
		for j in range(len(s.initial_values)):    
			# the iterative rule    
			tau = s.votes_eval(j)
			attacking_set = s.attack_relations[:,j]
			attacking_pos = np.where(attacking_set)
			temp1 = np.subtract(np.ones(s.var),current_iter)
			temp2 = np.take(temp1,attacking_pos)
			# the support relations are considered here 
			support_set = s.support_relations[:j]
			supporting_pos = np.where(support_set)
			temp3 = np.take(temp1,supporting_pos)
			current_iter[j] = tau*(1 + (np.prod(temp2)*np.prod(temp3)) - np.prod(temp3))

		save_iterations[i,:] = current_iter
		diff1 = np.subtract(save_iterations[i-1,:],save_iterations[i,:])
		condition = (np.absolute(diff1) < 0.00000001).prod()
		diff2 = np.sum(np.absolute(diff1))

	if condition == 1:
		s.time = time.time() - t0
		s.iterations_needed = i
		print("Converged!")
		s.results = str(1)
	else:
		print("Ran out of iterations!")
		s.time = 0
		s.iterations_needed = 0
		s.results = str(0)

def doEbsaf(s, iters=10000):
	t0 = time.time()
	save_iterations = np.zeros(shape = (iters+1,len(s.initial_values)))
	save_iterations [0,:] = s.initial_values
	i = 0
	condition = 0
	while (condition == 0 and i < iters+1):
		current_iter = copy.deepcopy(save_iterations[i,:])
		i +=  1
		for j in range(len(s.initial_values)):        
			tau = s.votes_eval(j)
			# the attacking arguments
			attacking_set = s.attack_relations[:,j]
			attacking_pos = np.transpose(np.nonzero(attacking_set)).tolist()
			attacking_pos = [item for sublist in attacking_pos for item in sublist]
			temp1 = []
			# votes for the attacking arguments
			for attacker in attacking_pos:
				if (attacker, j) in s.votes_relations:
					tau_relations = s.votes_relations_eval(attacker, j)
					temp1.append(1 - (tau_relations*current_iter[attacker]))
			# the supporting arguments
			supporting_set = s.support_relations[:,j]
			supporting_pos = np.transpose(np.nonzero(supporting_set)).tolist()
			supporting_pos = [item for sublist in supporting_pos for item in sublist]
			temp2 = []
			# votes on the support relations
			for supporter in supporting_pos:
				if (supporter, j) in s.votes_support_relations:
					tau_relations = s.votes_support_relations_eval(supporter, j)
					temp2.append(1 - (tau_relations*current_iter[supporter]))
			current_iter[j] = tau*(1+(np.prod(temp1)*np.prod(temp2)-np.prod(temp2)))
		save_iterations[i,:] = current_iter
		diff1 = np.subtract(save_iterations[i-1,:],save_iterations[i,:])
		condition = (np.absolute(diff1) < 0.0000000001).prod()
		diff2 = np.sum(np.absolute(diff1))

	if condition == 1:
		s.time = time.time() - t0
		s.iterations_needed = i
		print("Converged!")
		s.results = str(1)
	else:
		print("Ran out of iterations!")
		s.time = 0
		s.iterations_needed = 0
		s.results = str(0)