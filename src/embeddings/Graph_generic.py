
# Doesn't yet work with embiggen versions installed
#
try:
   import silence_tensorflow.auto
except:
   pass
import numpy as np
import sys

from ensmallen_graph import EnsmallenGraph
if len(sys.argv)!=4:
    sys.exit()
edge = sys.argv[1]
node = sys.argv[2]
out = sys.argv[3]

graph = EnsmallenGraph.from_unsorted_csv(
    edge_path=edge,
    node_path=node,
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
file1 = open(f"{out}_degrees.txt","ab")
np.save(file1, degrees)
file1.close() 

nodes = graph.nodes()
file2 = open(f"{out}_nodes.txt","a") 
file2.write(nodes)
file2.close() 

