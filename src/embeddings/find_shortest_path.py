import networkx as nx
import pandas as pd


#kg = nx.Graph()
#edges = nx.read_edgelist('../IMGVR/merged_imgvr_mg_edges.tsv')
#nodes = nx.read_adjlist("../IMGVR/merged_imgvr_mg_nodes.tsv")
#kg.add_edges_from(edges.edges())
#kg.add_nodes_from(nodes)
#nx.draw(kg, with_labels=True, font_weight='bold')

df = pd.read_csv('../IMGVR/merged_imgvr_mg_edges.tsv', sep="\t")


Graphtype = nx.Graph()
G = nx.from_pandas_edgelist(df, source='subject', target="object", create_using=Graphtype)

nx.shortest_path(G, source="GOLD:marine", target="GOLD:nasopharyngeal")

nx.shortest_path(G, source="GOLD:marine", target="GOLD:deep_ocean")

nx.shortest_path(G, source="GOLD:marine", target="GOLD:usa_columbia_river_estuary")
