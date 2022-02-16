from SGD_MDS2 import SGD_MDS2
from SGD_MDS import SGD_MDS
from MDS_classic import MDS
import modules.distance_matrix as distance_matrix
import modules.layout_io as layout_io

import numpy as np
import graph_tool.all as gt
import scipy.io

from metrics import get_neighborhood, get_norm_stress
from sklearn.metrics import pairwise_distances


#G.save('graphs/dummyblock.dot')

# G = gt.Graph(directed=False)
# G.add_vertex(3)
# G.add_edge_list([(0,1),(1,2),(2,0)])

#G = gt.generate_sbm(list(bm), probs, out_degs=None, directed=False, micro_ers=False, micro_degs=False)


#G = gt.load_graph("graphs/dwt_419.dot")
G = gt.lattice([10,10])
H = gt.lattice([5,20])
G = gt.graph_union(G,H)
G.add_edge_list([(52,103)])
G = gt.load_graph('graphs/mesh3e1.dot')
# G = gt.load_graph('graphs/btree8.dot')
d = distance_matrix.get_distance_matrix(G,'spdm',normalize=False)
d_norm = distance_matrix.get_distance_matrix(G,'spdm',normalize=True,verbose=False)

def get_w(k=5,a=5):
    A = gt.adjacency(G).toarray()
    mp = np.linalg.matrix_power
    #A = sum([mp(A,i) for i in range(1,a)])
    A = np.linalg.matrix_power(A,a)

    A += np.random.normal(scale=0.01,size=A.shape)
    #A = 1-d_norm

    #k = 10
    k_nearest = [np.argpartition(A[i],-k)[-k:] for i in range(len(A))]

    n = G.num_vertices()
    N = 0
    w = np.asarray([[ 0 if i != j else 0 for i in range(len(A))] for j in range(len(A))])
    for i in range(len(A)):
        for j in k_nearest[i]:
            if i != j:
                w[i][j] = 1
                w[j][i] = 1


    return w

# for i in range(len(w)):
#     for j in range(i):
#         if w[i][j] == 1:
#             N += 1

# Nc = (n*(n-1))/2 - N
#t = (N/Nc)*np.median(d)*0.1
t = 0.7


# for k in K:
#     k = k if k < G.num_vertices() else G.num_vertices()
#     w = get_w(k)
#     for t in T:



print(G.num_vertices())



k = 8
a = int(np.max(d))

print(np.max(d))
for a in [15]:
    w = get_w(k=8,a=a)
    #w = gt.adjacency(G).toarray()

    count = 0
    temp_stress = 0

    t = np.count_nonzero(w)/w.size
    t = 0.1
    Y = SGD_MDS2(d,weighted=True,w=w)
    Xs = Y.solve(num_iter=400,t=t,debug=True)
    Zx = Xs[-1]

    X = layout_io.normalize_layout(Zx)
    print("Stress: ", get_norm_stress(X,d_norm))
    print("NP: ", get_neighborhood(X,d,2))


    pos = G.new_vp('vector<float>')
    pos.set_2d_array(Zx.T)
    #
    gt.graph_draw(G,pos=pos)


    for count in range(len(Xs)):
        if count % 1 == 0:
            layout = Xs[count]
            X = layout_io.normalize_layout(layout)
            print(get_neighborhood(X,d))

            pos = G.new_vp('vector<float>')
            pos.set_2d_array(X.T)
            #
            gt.graph_draw(G,pos=pos,output='drawings/t_mesh_k_' + str(k) + '_a' + str(a) + '_' +str(count) + '.png')
