from saafNew import *
import csv


all_data = []

for i in range(1000):
	print("Running trial : ", i)
	np.random.seed(i) #change seed each time, i fixes it, noarg randomises
	nodes = np.random.randint(1,1001)
	d_A = np.random.uniform(0.001,0.01)
	s = Structure(var = nodes, density = d_A)
	s.randomInit()
	doEsaf(s)
	all_data.append([str(s.var), str(s.density), str(s.results), str(s.time), str(s.iterations_needed)])

with open('test_ld.csv', 'a') as myfile:
	wr = csv.writer(myfile)
	wr.writerows(all_data)

all_data = []

for i in range(1000):
	print("Running trial : ", i)
	np.random.seed(i) #change seed each time, i fixes it, noarg randomises
	nodes = np.random.randint(1,1001)
	d_A = np.random.uniform(0.01,0.1)
	s = Structure(var = nodes, density = d_A)
	s.randomInit()
	doEsaf(s)
	all_data.append([str(s.var), str(s.density), str(s.results), str(s.time), str(s.iterations_needed)])

with open('test_md.csv', 'a') as myfile:
	wr = csv.writer(myfile)
	wr.writerows(all_data)

all_data = []


for i in range(1000):
	print("Running trial : ", i)
	np.random.seed(i) #change seed each time, i fixes it, noarg randomises
	nodes = np.random.randint(1,1001)
	d_A = np.random.uniform(0.1,1)
	s = Structure(var = nodes, density = d_A)
	s.randomInit()
	doEsaf(s)
	all_data.append([str(s.var), str(s.density), str(s.results), str(s.time), str(s.iterations_needed)])

with open('test_hd.csv', 'a') as myfile:
	wr = csv.writer(myfile)
	wr.writerows(all_data)





all_data = []

for i in range(1000):
	print("Running trial : ", i)
	np.random.seed(i) #change seed each time, i fixes it, noarg randomises
	nodes = np.random.randint(1,100)
	d_A = np.random.uniform(0,1)
	s = Structure(var = nodes, density = d_A)
	s.randomInit()
	doEsaf(s)
	all_data.append([str(s.var), str(s.density), str(s.results), str(s.time), str(s.iterations_needed)])

with open('test_ld1.csv', 'a') as myfile:
	wr = csv.writer(myfile)
	wr.writerows(all_data)

all_data = []

for i in range(1000):
	print("Running trial : ", i)
	np.random.seed(i) #change seed each time, i fixes it, noarg randomises
	nodes = np.random.randint(100,300)
	d_A = np.random.uniform(0,1)
	s = Structure(var = nodes, density = d_A)
	s.randomInit()
	doEsaf(s)
	all_data.append([str(s.var), str(s.density), str(s.results), str(s.time), str(s.iterations_needed)])

with open('test_md1.csv', 'a') as myfile:
	wr = csv.writer(myfile)
	wr.writerows(all_data)

all_data = []

for i in range(1000):
	print("Running trial : ", i)
	np.random.seed(i) #change seed each time, i fixes it, noarg randomises
	nodes = np.random.randint(300,1001)
	d_A = np.random.uniform(0,1)
	s = Structure(var = nodes, density = d_A)
	s.randomInit()
	doEsaf(s)
	all_data.append([str(s.var), str(s.density), str(s.results), str(s.time), str(s.iterations_needed)])

with open('test_hd1.csv', 'a') as myfile:
	wr = csv.writer(myfile)
	wr.writerows(all_data)








