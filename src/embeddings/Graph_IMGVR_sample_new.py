try:
   import silence_tensorflow.auto
except:
   pass
import numpy as np

from ensmallen_graph import EnsmallenGraph

graph = EnsmallenGraph.from_unsorted_csv(
    edge_path="/global/scratch/marcin/N2V/embiggen/notebooks/IMGVR/IMGVR_sample_KGX_edges.tsv",
    node_path="/global/scratch/marcin/N2V/embiggen/notebooks/IMGVR/IMGVR_sample_KGX_nodes.tsv",
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
print(degrees)
file1 = open("IMGVR_sample_ensmallen_degrees.txt","a") 
np.save(file1, degrees)
file1.close() 

nodes = graph.nodes()
file2 = open("IMGVR_sample_ensmallen_nodes.txt","a") 
file2.write(nodes)
file2.close() 

