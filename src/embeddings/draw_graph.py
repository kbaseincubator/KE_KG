import networkx as nx
import pandas as pd

from matplotlib import pylab
import matplotlib.pyplot as plt

df = pd.read_csv('../IMGVR/merged_imgvr_mg_edges.tsv', sep="\t")

df.head()

Graphtype = nx.Graph()
G = nx.from_pandas_edgelist(df, source='subject', target="object", create_using=Graphtype)


def save_graph(graph, file_name):
    # initialze Figure
    plt.figure(num=None, figsize=(20, 20), dpi=80)
    plt.axis('off')
    fig = plt.figure(1)
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph, pos)
    nx.draw_networkx_edges(graph, pos)
    nx.draw_networkx_labels(graph, pos)

    #cut = 1.00
    #xmax = cut * max(xx for xx, yy in pos.values())
    #ymax = cut * max(yy for xx, yy in pos.values())
    #plt.xlim(0, xmax)
    #plt.ylim(0, ymax)

    plt.savefig(file_name, bbox_inches="tight")
    pylab.close()
    del fig



save_graph(G,"merged_imgvr_mg_edges.pdf")

