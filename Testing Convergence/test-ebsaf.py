from saafEbsaf import *
import csv

data = ['args','dA','dS','res','time','iters']
with open("output_bsaf.csv", "a") as fp:
	wr = csv.writer(fp, dialect='excel')
	wr.writerow(data)

for i in range(1000):
	print("Running trial : ", i)
	nodes = np.random.randint(2,1001)
	d_A = np.random.uniform(0.15,0.5)
	d_S = np.random.uniform(0.1,0.2)
	s = Structure(var = nodes, density = d_A, support_density=d_S, epsilon = 0.1)
	s.randomInit()
	print("running Bsaf")
	doBsaf(s)
	data = [str(s.var), str(s.density), str(s.support_density), str(s.results), str(s.time), str(s.iterations_needed)]
	with open("output_bsaf.csv", "a") as fp:
		wr = csv.writer(fp, dialect='excel')
		wr.writerow(data)

data = ['args','dA','dS','res','time','iters']
with open("output_ebsaf.csv", "a") as fp:
	wr = csv.writer(fp, dialect='excel')
	wr.writerow(data)

for i in range(1000):
	print("Running trial : ", i)
	nodes = np.random.randint(2,1001)
	d_A = np.random.uniform(0.15,0.5)
	d_S = np.random.uniform(0.1,0.2)
	s = Structure(var = nodes, density = d_A, support_density=d_S, epsilon = 0.1)
	s.randomInit()
	print("running Ebsaf")
	doEbsaf(s)
	data = [str(s.var), str(s.density), str(s.support_density), str(s.results), str(s.time), str(s.iterations_needed)]
	with open("output_ebsaf.csv", "a") as fp:
		wr = csv.writer(fp, dialect='excel')
		wr.writerow(data)
