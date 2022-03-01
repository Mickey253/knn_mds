import numpy as np
import graph_tool.all as gt
import matplotlib.pyplot as plt
import pickle

import modules.layout_io as layout_io
import modules.graph_io as graph_io
import modules.distance_matrix as distance_matrix

norm = lambda x: np.linalg.norm(x,ord=2)

def choose(n,k):
    product = 1
    for i in range(1,k+1):
        product *= (n-(k-1))/i
    return product

def dist(X,d):
    stress = 0
    for i in range(len(X)):
        for j in range(i):
            stress += abs(np.linalg.norm(X[i]-X[j])-d[i][j])/d[i][j]
    return stress/choose(len(X),2)

def get_neighborhood(X,d,rg = 1):
    """
    How well do the local neighborhoods represent the theoretical neighborhoods?
    Closer to 1 is better.
    Measure of percision: ratio of true positives to true positives+false positives
    """
    def get_k_embedded(X,k_t):
        dist_mat = [[norm(X[i]-X[j]) if i != j else 10000 for j in range(len(X))] for i in range(len(X))]
        return [np.argpartition(dist_mat[i],len(k_t[i]))[:len(k_t[i])] for i in range(len(dist_mat))]

    k_theory = [np.where((d[i] <= rg) & (d[i] > 0))[0] for i in range(len(d))]
    k_embedded = get_k_embedded(X,k_theory)

    sum = 0
    for i in range(len(X)):
        count_intersect = 0
        for j in range(len(k_theory[i])):
            k = len(k_theory[i])
            if k_theory[i][j] in k_embedded[i]:
                count_intersect += 1
        sum += count_intersect/(2*k - count_intersect)

    return sum/len(X)

def stress(X,d):
    stress = 0
    for i in range(len(X)):
        for j in range(i):
            stress += pow(np.linalg.norm(X[i]-X[j])-d[i][j],2)
    return pow(stress,0.5)

with open('data/test_low6.pkl', 'rb') as myfile:
    data = pickle.load(myfile)

print(data.keys())

graph = data['jazz.dot']

metric = 'NP'

#tsnet = graph['tsnet'][metric]
#SGD = graph['SGD'][metric]
LG_low = graph['LG_low'][metric]
LG_high = graph['LG_high'][metric]



# plt.plot([1 for _ in range(5)],LG_low,'o',label="LG_low")
# plt.plot([2 for _ in range(5)],LG_high,'o',label="LG_high")
#
#
# plt.legend()
# plt.show()
# plt.clf()

row_labels = list(data.keys())
column_labels = ["k=8","k= |V|"]

cell_data = []
count_tsnet, count_sgd = 0,0
for row in row_labels:
    if data[row]['LG_low'][metric][0] != None:
        tsnet = np.array(data[row]['LG_low'][metric]).mean()
        sgd = np.array(data[row]['LG_high'][metric]).mean()
        if tsnet < sgd:
            count_tsnet += 1
        else:
            count_sgd += 1
        cell_data.append([round(tsnet,5),round(sgd,5)])
    else:
        cell_data.append([0,0])

print("low performed better on ", count_tsnet)
print("hgih performed better on ", count_sgd)

plt.suptitle("NP")
plt.table(cellText=cell_data,
                      rowLabels=row_labels,
                      colLabels=column_labels,
                      loc=None,
                      colWidths=[0.2,0.2,0.2],
                      cellLoc='center')
plt.xticks([])
plt.yticks([])
plt.axis('off')

plt.show()
