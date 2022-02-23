from SGD_MDS2 import SGD_MDS2
from SGD_MDS import SGD_MDS
from MDS_classic import MDS
import modules.distance_matrix as distance_matrix
import modules.layout_io as layout_io

import matplotlib.pyplot as plt
import numpy as np
import graph_tool.all as gt
import scipy.io

from metrics import get_neighborhood, get_norm_stress
from sklearn.metrics import pairwise_distances


def display_stats(graph):
    G = gt.load_graph('graphs/{}.dot'.format(graph))
    d = distance_matrix.get_distance_matrix(G,'spdm',normalize=False)

    print(graph)
    print("num_vertices", G.num_vertices())
    print("num_edges",G.num_edges())
    print("diameter", np.max(d))
    print("global clustering coefficient", gt.global_clustering(G))
    print("average local clustering coefficient", sum(gt.local_clustering(G))/G.num_vertices())
    print("average degree", gt.vertex_average(G,'total'))
    print("edges/nodes", G.num_edges()/G.num_vertices())

    print()


display_stats('price_1000')
display_stats('rajat11')
display_stats('block_2000')
display_stats('oscil')
