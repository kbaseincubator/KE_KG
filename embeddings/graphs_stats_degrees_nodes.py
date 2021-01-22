import numpy as np
from ensmallen_graph import EnsmallenGraph

graph = EnsmallenGraph.from_unsorted_csv(
    edge_path="../IMGVR/IMGVR_sample_KGX_edges.tsv",
    node_path="../IMGVR/IMGVR_sample_KGX_nodes.tsv",
    sources_column="subject",
    destinations_column="object",
    nodes_column = 'id',
    #node_types_column = 'category',
    #default_node_type = 'biolink:NamedThing',
    directed=False
    #weights_column="weight"
)

#print(graph.report())
print(graph)


degrees = graph.degrees()
np.savetxt("IMGVR_sample_degrees.csv", degrees, delimiter="\t")
nodes = graph.get_node_names()
np.savetxt("IMGVR_sample_nodes.csv", degrees, delimiter="\t")
