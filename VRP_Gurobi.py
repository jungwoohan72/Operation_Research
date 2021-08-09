import numpy as np
import matplotlib.pyplot as plt

from gurobipy import Model, GRB, quicksum

rnd = np.random
rnd.seed(4)

n = 10 # number of clients

# 200 by 100 box
xc = rnd.rand(n+1)*200 # x-coordinates (1 extra for the depot)
yc = rnd.rand(n+1)*100

N = [i for i in range(1,n+1)] # Clients
V = [0] + N # Clients with the depot
A = [(i,j) for i in V for j in V if i!=j] # Edge
c = {(i,j): np.hypot(xc[i]-xc[j], yc[i]-yc[j]) for i,j in A}
Q = 20 # Vehicle capacity
q = {i: rnd.randint(1,10) for i in N} # Customer demand

mdl = Model('CVRP')
x = mdl.addVars(A, vtype = GRB.BINARY)
u = mdl.addVars(N, vtype = GRB.CONTINUOUS)

mdl.modelSense = GRB.MINIMIZE
mdl.setObjective(quicksum(x[i,j]*c[i,j] for i,j in A))

mdl.addConstrs(quicksum(x[i,j] for j in V if j!=i) == 1 for i in N);
mdl.addConstrs(quicksum(x[i,j] for i in V if j!=i) == 1 for j in N);
mdl.addConstrs((x[i,j] == 1) >> (u[i] + q[i] == u[j]) for i,j in A if i != 0 and j != 0);
mdl.addConstrs(u[i]>=q[i] for i in N);
mdl.addConstrs(u[i]<=Q for i in N);

mdl.optimize()

active_arcs = [a for a in A if x[a].x > 0.99]
print(active_arcs)
print(u)


plt.figure()
for i,j in active_arcs:
    plt.plot([xc[i], xc[j]], [yc[i],yc[j]], c = 'g', zorder = 0)
plt.plot(xc[0], yc[0], c='r', marker='s')
plt.scatter(xc[1:], yc[1:], c='b')
plt.show()